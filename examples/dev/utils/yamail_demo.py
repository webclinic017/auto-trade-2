import yamail

smtp = yamail.SMTP(host='smtp.qq.com',   # 邮箱的服务器
                   user='135*****@qq.com',  # 发送邮箱用的用户名
                   password='')   # qq邮箱需要授权码,授权码需要在邮箱的设置-帐户-POP3/SMTP服务（开启服务）
files = ["C:/Users/admin/Desktop/uid.txt"]
smtp.send(to=['152****@qq.com'],  # 发送给谁,如果是多少，就在list中添加多个
          cc=['285*****@qq.com'],  # 抄送给谁,如果是多少，就在list中添加多个
          subject='邮件主题',  # 邮件主题
          contents='邮件正文',  # 邮件正文
          attachments=files)  # 附件，如果有多个附件，写list中
smtp.close()