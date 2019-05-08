from django.db import models


# Create your models here.
# 用户表
class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=64, unique=True, verbose_name='名字')
    password = models.CharField(max_length=250, verbose_name='密码')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    sex = models.CharField(max_length=32, choices=gender, default='男', verbose_name='性别')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = verbose_name


# 业务线
class BusinessUnit(models.Model):
    parent_unit = models.ForeignKey('self', 'on_delete', null=True, blank=True, related_name='parent_level')
    name = models.CharField(max_length=64, unique=True, verbose_name='业务线')
    memo = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = verbose_name


# 合同
class Contract(models.Model):
    sn = models.CharField(max_length=128, unique=True, verbose_name='合同号')
    name = models.CharField(max_length=64, verbose_name='合同名称')
    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    price = models.IntegerField(verbose_name='合同金额')
    detail = models.TextField(null=True, blank=True, verbose_name='合同详细')
    start_day = models.DateField(null=True, blank=True, verbose_name='开始日期')
    end_day = models.DateField(null=True, blank=True, verbose_name='失效日期')
    license_num = models.IntegerField(null=True, blank=True, verbose_name='license数量')
    c_day = models.DateField('创建日期', auto_now_add=True)
    m_day = models.DateField('修改日期', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = verbose_name


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='标签名')
    c_day = models.DateField(auto_now_add=True, verbose_name='创建日期')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


# 所有资产的共有数据表
class Asset(models.Model):
    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('securitydevice', '安全设备'),
    )

    asset_status = (
        (0, '在线'),
        (1, '下线'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
    )

    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server', verbose_name='资产类型')
    name = models.CharField(max_length=64, unique=True, verbose_name='资产名称')
    sn = models.CharField(max_length=128, unique=True, verbose_name='资产序列号')
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE, null=True, blank=True,
                                      verbose_name='所属业务线')
    status = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='设备状态')

    manufacturer = models.CharField(max_length=128, null=True, verbose_name='制造商')
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='资产管理员',
                              related_name='user')
    idc = models.CharField(max_length=128, null=True, verbose_name='所在机房')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True, verbose_name='合同')

    purchase_day = models.DateField(null=True, blank=True, verbose_name='购买日期')
    expire_day = models.DateField(null=True, blank=True, verbose_name='过保日期')
    price = models.FloatField(null=True, blank=True, verbose_name='价格')

    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='批准人',
                                    related_name='approved_by')

    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='批准日期')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    def __str__(self):
        return '<%s>  %s' % (self.get_asset_type_display(), self.name)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = verbose_name
        ordering = ['-c_time']


# 服务器设备
class Server(models.Model):
    sub_asset_type_choice = (
        (0, 'PC服务器'),
        (1, '刀片机'),
        (2, '小型机'),
    )

    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入'),
    )

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='服务器类型')
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name='添加方式')
    hosted_on = models.ForeignKey('self', 'on_delete', related_name='hosted_on_server',
                                  blank=True, null=True, verbose_name='宿主机')
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='服务器型号')
    raid_type = models.CharField(max_length=512, null=True, blank=True, verbose_name='Raid类型')

    os_type = models.CharField(max_length=64, null=True, blank=True, verbose_name='操作系统类型')
    os_distribution = models.CharField(max_length=64, null=True, blank=True, verbose_name='发行版本')
    os_release = models.CharField(max_length=64, null=True, blank=True, verbose_name='操作系统版本')

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = verbose_name


# 安全设备
class SecurityDevice(models.Model):
    sub_asset_type_choice = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (4, '运维审计系统'),
    )

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name='安全设备类型')

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + " id:%s" % self.id

    class Meta:
        verbose_name = '安全设备'
        verbose_name_plural = verbose_name


# 存储设备
class StorageDevice(models.Model):
    sub_asset_type_choice = (
        (0, '磁盘阵列'),
        (1, '网络存储器'),
        (2, '磁带库'),
        (4, '磁带机'),
    )

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="存储设备类型")

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + " id:%s" % self.id

    class Meta:
        verbose_name = '存储设备'
        verbose_name_plural = verbose_name


# 网络设备
class NetworkDevice(models.Model):
    sub_asset_type_choice = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (4, 'VPN设备'),
    )

    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="网络设备类型")

    vlan_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='VLanIP')
    intranet_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='内网IP')

    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='网络设备型号')
    firmware = models.CharField(max_length=128, null=True, blank=True, verbose_name='设备固件版本')
    port_num = models.SmallIntegerField(null=True, blank=True, verbose_name='端口个数')
    device_detail = models.TextField(null=True, blank=True, verbose_name='详细配置')

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = verbose_name


# 只保存付费购买的软件
class Software(models.Model):
    sub_asset_type_choice = (
        (0, '操作系统'),
        (1, '办公\开发软件'),
        (2, '业务软件'),
    )

    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="软件类型")
    license_num = models.IntegerField(default=1, verbose_name='授权数量')
    version = models.CharField(max_length=64, unique=True, help_text='例如: CentOS release 6.7 (Final)',
                               verbose_name='软件/系统版本')

    def __str__(self):
        return '%s--%s' % (self.get_sub_asset_type_display(), self.version)

    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = verbose_name


# CPU组件
class CPU(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)  # 设备上的cpu肯定都是一样的，所以不需要建立多个cpu数据，一条就可以，因此使用一对一。
    cpu_model = models.CharField(max_length=128, null=True, blank=True, verbose_name='CPU型号')
    cpu_count = models.PositiveSmallIntegerField(default=1, verbose_name='物理CPU个数')
    cpu_core_count = models.PositiveSmallIntegerField(default=1, verbose_name='CPU核数')

    def __str__(self):
        return self.asset.name + ":   " + self.cpu_model

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = "CPU"


# 内存组件
class RAM(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)  # 只能通过外键关联Asset。否则不能同时关联服务器、网络设备等等。
    sn = models.CharField(max_length=128, null=True, blank=True, verbose_name='SN号')
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='内存型号')
    manufacturer = models.CharField(max_length=128, null=True, blank=True, verbose_name='内存制造商')
    slot = models.CharField(max_length=64, verbose_name='插槽')
    capacity = models.IntegerField(null=True, blank=True, verbose_name='内存大小(GB)')

    def __str__(self):
        return '%s: %s: %s: %s' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = '内存'
        verbose_name_plural = "内存"
        unique_together = ('asset', 'slot')  # 同一资产下的内存，根据插槽的不同，必须唯一


# 存储设备
class Disk(models.Model):
    disk_interface_type_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
        ('unknown', 'unknown'),
    )

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    sn = models.CharField(max_length=128, verbose_name='硬盘SN号')
    slot = models.CharField(max_length=64, null=True, blank=True, verbose_name='所在插槽位')
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='磁盘型号')
    manufacturer = models.CharField(max_length=128, null=True, blank=True, verbose_name='磁盘制造商')
    capacity = models.FloatField(null=True, blank=True, verbose_name='磁盘容量(GB)')
    interface_type = models.CharField(max_length=16, choices=disk_interface_type_choice, default='unknown',
                                      verbose_name='接口类型')

    def __str__(self):
        return '%s:  %s:  %s:  %sGB' % (self.asset.name, self.model, self.slot, self.capacity)

    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = verbose_name
        unique_together = ('asset', 'sn')


# 网卡组件
class NIC(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name='网卡名称')
    model = models.CharField(max_length=128, verbose_name='网卡型号')
    mac = models.CharField(max_length=64, verbose_name='MAC地址')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    net_mask = models.CharField(max_length=64, null=True, blank=True, verbose_name='掩码')
    bonding = models.CharField(max_length=64, null=True, blank=True, verbose_name='绑定地址')

    def __str__(self):
        return '%s:  %s:  %s' % (self.asset.name, self.model, self.mac)

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = verbose_name
        unique_together = ('asset', 'model', 'mac')  # 资产、型号和mac必须联合唯一。防止虚拟机中的特殊情况发生错误。


# 新资产待审批区
class NewAssetApprovalZone(models.Model):
    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('securitydevice', '安全设备'),
        ('software', '软件资产'),
    )
    sn = models.CharField(max_length=128, unique=True, verbose_name='资产SN号')  # 此字段必填
    asset_type = models.CharField(choices=asset_type_choice, default='server', max_length=64, blank=True, null=True,
                                  verbose_name='资产类型')

    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name='生产厂商')
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name='型号')
    ram_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='内存大小')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU型号')
    cpu_count = models.PositiveSmallIntegerField(blank=True, null=True)
    cpu_core_count = models.PositiveSmallIntegerField(blank=True, null=True)
    os_distribution = models.CharField(max_length=64, blank=True, null=True)
    os_type = models.CharField(max_length=64, blank=True, null=True)
    os_release = models.CharField(max_length=64, blank=True, null=True)

    data = models.TextField('资产数据')  # 此字段必填

    c_time = models.DateTimeField('汇报日期', auto_now_add=True)
    m_time = models.DateTimeField('数据更新日期', auto_now=True)
    approved = models.BooleanField('是否批准', default=False)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = verbose_name
        ordering = ['-c_time']


# 事件记录
class EventLog(models.Model):
    event_type_choice = (
        (0, '其它'),
        (1, '硬件变更'),
        (2, '新增配件'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '业务上线\更新\变更'),
    )
    name = models.CharField(max_length=128, verbose_name='事件名称')
    asset = models.ForeignKey(Asset, null=True, blank=True, on_delete=models.SET_NULL)
    new_asset = models.ForeignKey(NewAssetApprovalZone, blank=True, null=True,
                                  on_delete=models.SET_NULL)  # 当资产审批失败时有这项数据
    event_type = models.SmallIntegerField(choices=event_type_choice, default=4, verbose_name='事件类型')
    component = models.CharField(max_length=256, blank=True, null=True, verbose_name='事件子项')
    detail = models.TextField(verbose_name='事件详情')
    date = models.DateTimeField(auto_now_add=True, verbose_name='事件时间')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='事件执行人',
                             on_delete=models.SET_NULL)  # 自动更新资产数据时没有执行人
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = verbose_name
