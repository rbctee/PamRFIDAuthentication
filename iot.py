import spwd
import crypt
import sys
import sqlite3
import os
from datetime import datetime

sd = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, '/usr/local/lib/python2.7/dist-packages/')
sys.path.append(sd)

import requests
from secret import BOT_TOKEN, BOT_CHAT_ID

db_file = os.path.join(sd, "rfids.db")

def telegram_bot_sendtext(bot_message):
   send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + BOT_CHAT_ID + '&parse_mode=Markdown&text=' + bot_message
   response = requests.get(send_text)

   return response.json()

def check_rfid(name, rfid):
  conn = None
  try:
      conn = sqlite3.connect(db_file)
      cur = conn.cursor()

      cur.execute("SELECT DISTINCT names.name,identifiers.rfid FROM names INNER JOIN identifiers on names.name = identifiers.name")
      rows = cur.fetchall()

      for row in rows:
          db_name, db_rfid = row

          if db_name == name and db_rfid == rfid:
            return True
  except Exception as e:
      print(e)
  
  return False

def check_pw(user, password):
    """Check the password matches local unix password on file"""
    hashed_pw = spwd.getspnam(user)[1]
    return crypt.crypt(password, hashed_pw) == hashed_pw

def pam_sm_authenticate(pamh, flags, argv):
    try:
      user = pamh.get_user()
    except pamh.exception as e:
      return e.pam_result
    if not user:
      return pamh.PAM_USER_UNKNOWN

    try:
      import serial

      ser = serial.Serial()
      ser.baudrate = 115200
      ser.port = '/dev/ttyUSB0'
      ser.open()

      print("Waiting for RFID card ...")
      ser.write(bytearray([1]))
      rfid = ser.read(8)
      # print "Checking id", rfid

      if check_rfid(user, rfid):
        print('Success')

        now = datetime.now()
        telegram_bot_sendtext("User '%s' authenticated with an RFID card at %s" % (user, now.strftime("%d/%m/%Y %H:%M:%S")))

        ser.write(bytearray([2]))
        return pamh.PAM_SUCCESS
      else:
        ser.write(bytearray([3]))
        return pamh.PAM_AUTH_ERR

    except Exception as e:
      # print(e)
      # print("Error! Continuing with normal authentication")
      try:
        resp = pamh.conversation(pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "Password: "))
      except pamh.exception as e:
        return e.pam_result

      if not check_pw(user, resp.resp):
        return pamh.PAM_AUTH_ERR

    return pamh.PAM_SUCCESS

def pam_sm_setcred(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_acct_mgmt(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
  return pamh.PAM_SUCCESS
