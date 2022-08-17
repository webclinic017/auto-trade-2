import uiautomator2 as u2

device = u2.connect()
print(device.address)
print(device.device_info)
