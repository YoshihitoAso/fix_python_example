import sys
import time
import logging
from datetime import datetime

import quickfix as fix

from model.logger import setup_logger

__SOH__ = chr(1)

setup_logger('logfix', 'Logs/message.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    """FIX Application"""
    execID = 0

    def __init__(self):
        super().__init__()
        self.sessionID = None

    def onCreate(self, sessionID):
        """onCreate"""
        print("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        """onLogon"""
        self.sessionID = sessionID
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        """onLogout"""
        print("Session (%s) logout !" % sessionID.toString())
        return

    def toAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Admin) S >> %s" % msg)
        return

    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Admin) R << %s" % msg)
        return

    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(App) S >> %s" % msg)
        return

    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(App) R << %s" % msg)
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        pass

    def genExecID(self):
        self.execID += 1
        return str(self.execID).zfill(5)

    def put_new_order(self):
        """Request sample [New-Order-Single]"""
        message = fix.Message()
        header = message.getHeader()

        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))  # 39 = D

        message.setField(fix.ClOrdID(self.genExecID()))  # 11 = Unique Sequence Number
        message.setField(fix.Side(fix.Side_BUY))  # 43 = 1 BUY
        message.setField(fix.Symbol("MSFT"))  # 55 = MSFT
        message.setField(fix.OrderQty(10000))  # 38 = 10000
        message.setField(fix.Price(100))  # 44 = 100
        message.setField(fix.OrdType(fix.OrdType_LIMIT))  # 40 = 2 Limit Order
        message.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))  # 21 = 3
        message.setField(fix.TimeInForce('0'))
        message.setField(fix.Text("NewOrderSingle"))
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        message.setField(trstime)

        fix.Session.sendToTarget(message, self.sessionID)

    def run(self):
        while 1:
            options = str(input("Please choose 1 for Put New Order or 2 for Exit!\n"))
            if options == '1':  # Put New Order
                self.put_new_order()
                print("Done: Put New Order\n")
                continue
            if options == '2':  # Exit
                sys.exit(0)
            else:
                print("Valid input is 1 for order, 2 for exit\n")
            time.sleep(2)
