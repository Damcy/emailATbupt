#!/usr/bin/env python3
# author: Ian
# email: stmayue@gmail.com
# description: send mail at BUPT
import os
import sys
import json
import traceback
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self, conf):
        try:
            self.from_add = conf["from_address"]
            self.from_add_pwd = conf["from_address_pwd"]
            self.smtp = conf["smtp"]
            print("init mail success")
            self.is_ok = True
        except:
            sys.stderr.write("init mail failed!\n")
            print(trackback.format_ext())
            self.is_ok = False

    def send(self, subject, to_address_list, content=None, attach_file_path_list=None, attach_file_name_list=None):
        if not self.is_ok:
            return False
        mail_msg = MIMEMultipart()
        mail_msg["Subject"] = subject
        mail_msg["From"] = self.from_add
        mail_msg["To"] = ','.join(to_address_list)
        # content
        if content != None:
            mail_msg.attach(MIMEText(content, 'html', 'utf-8'))
        # attrchment
        if attach_file_path_list != None:
            if attach_file_name_list == None:
                sys.stderr.write("Attachments should have names!\n")
                return False
            if len(attach_file_path_list) != len(attach_file_name_list):
                sys.stderr.write("length of attach file != length of attachment's name\n")
                return False
            for i in range(0, len(attach_file_path_list)):
                attach = MIMEText(open(attach_file_path_list[i], 'rb').read(), 'base64', 'utf-8')
                attach["Content-Type"] = "application/octet-stream"
                des = "attachment; filename=\"" + attach_file_name_list[i] + "\""
                attach["Content-Disposition"] = des
                mail_msg.attach(attach)
        try:
            s = smtplib.SMTP()
            s.connect(self.smtp)
            s.login(self.from_add, self.from_add_pwd)
            s.sendmail(self.from_add, to_address_list, mail_msg.as_string())
            s.quit()
        except:
            print("Unable to send mail!")
            print(traceback.format_exc())
            return False
        return True


if __name__ == '__main__':
    subject = "测试"
    to_address_list = ['XXX@bupt.edu.cn', 'XXX@hotmail.com']
    # mail content
    content = "测试邮件"
    # attachment file path
    att_file_list = ['/home/my/before314/helloworld/analyse/pic/9.png', '/home/my/before314/helloworld/analyse/pic/99.png']
    # attachment file name with file suffixes
    att_file_name = ['9.png', '99.png']
    conf = {"from_address": "XXXX@bupt.edu.cn", "from_address_pwd": "XXXX", "smtp": "mail.bupt.edu.cn"}
    m = Mail(conf)
    m.send(subject, to_address_list, content=content, attach_file_path_list=att_file_list, attach_file_name_list=att_file_name)
