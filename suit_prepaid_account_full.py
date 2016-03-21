from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
from nose.tools import nottest
from nose.plugins.attrib import attr
import time
import datetime
import dateutil.parser
from gp_node.request_handler.request_handler import RequestHandler,timer
from gp_node.network.protocols.packets.slab_packet import SlabConfigurationPacket
from gp_node.network.protocols.packets.accounting_state_packet import AccountingStatePacket
import datetime
from gp_node.network.protocols.packets.bundle import Bundle

class testprepaid_account(object):
    
    @classmethod
    def setup_class(self):
        print "prepaid account test"
    	#self.test_handler = RequestHandler()        
    	self.testHandler = RequestHandler()
        self.testHandler.handle_network_request("set_power_limit:70000000")
        self.testHandler.handle_network_request("slab_disable")
        self.testHandler.handle_network_request("fd_disable")
    @classmethod
    def teardown_class(self):
        self.testHandler.kill()

    def setUp(self):
        """This method is run once before _each_ test method is executed"""
    	#self.testHandler = RequestHandler()
    	#self.testHandler.handle_network_request("deassert")	
    	#self.testHandler.handle_network_request("deassert")
    	self.testHandler.handle_network_request("fd_reset", validity_level="medium")
    	self.testHandler.handle_network_request("set_power_limit:9999999")
    	self.testHandler.handle_network_request("clear_account")


    def teardown(self):
        """This method is run once after _each_ test method is executed"""
    	self.testHandler.handle_network_request("deassert")	
    	self.testHandler.handle_network_request("deassert")

    
    '''@attr(speed='pos')
    def test_01_credit_deduction(self):
        """
       	TEST 1
        The test checks credits duduction with load"""
	print "...starting test 2.01"
	self.testHandler.handle_maxwell_request("voltage:0")
	print"clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="high")
	left_credits=float((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	print "credits left= ",left_credits
    	assert_equal(left_credits,0.0)
	self.testHandler.handle_network_request("slab_disable")
	print "slab disabled"
	self.testHandler.handle_network_request("fd_disable")
	print " fd disabled"
	self.testHandler.handle_network_request("set_credit_limit:0",validity_level="medium")
	credit_limit=self.testHandler.handle_network_request("get_credit_limit")
	print "credit limit = ",credit_limit
    	print "setting price=100"
	self.testHandler.handle_network_request("set_price:100")
	time.sleep(1)
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])	
	print "price=",price
	self.testHandler.handle_network_request("recharge:25",validity_level="medium")
	print "recharged with 25"
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits",validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	print "accurate credits = ",acc_crdts
	a=float(acc_crdts)
	print "with 1 kw load and credit=25 with price =100 the credit should unniformly decrease to zero in 15 minutes"
	energy_initial=float((self.testHandler.handle_network_request("get_active_energy", validity_level="high")).split(" ")[0])	
	print "initial  energy =",energy_initial
	# load is 1 kw so 1 unit should be deduccted in 3600 seconds
	current_time =  str(self.testHandler.handle_network_request("get_time"))
	dt1= datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
	print "in date format ",dt1
	print "setting load"
	self.testHandler.handle_maxwell_request("voltage:100")
	self.testHandler.handle_maxwell_request("phase_load:10")
	time.sleep(5)
	# a is float value of credit in accurate credits
	while(a>0.0):
		
		power=float((self.testHandler.handle_network_request("get_active_power",validity_level="medium")).split(" ")[0])
		print "active power =",power," watts"
		acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
		acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
		print "accurate credits = ",acc_crdts
		a=float(acc_crdts)
	self.testHandler.handle_maxwell_request("voltage:0")
	energy_final=float((self.testHandler.handle_network_request("get_active_energy", validity_level="high")).split(" ")[0])	
	print "initial  energy =",energy_final	
	current_time =  str(self.testHandler.handle_network_request("get_time"))
	dt2= datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
	print "in date format ",dt2
	print('credits left should be zero now')
	print "credit left ==",a
	assert_equal(a,0.0)
	d3=(dt2-dt1)
	print "time taken by the load to consume 25 cr @price=100 ",d3
	energy_consumed=(energy_final-energy_initial)
	print "energy consumed in this case = ",energy_consumed
    	#assert_between(energy_consumed,250,253)
	assert(250 <= energy_consumed <= 275)
	

    	
    @attr(speed='pos')
    def test_02_credit_deduction(self):
        """
        TEST 2
        The test checks credits duduction on load with power cycle
        """
        print "...starting test 2.02"
        self.testHandler.handle_maxwell_request("voltage:0")
	print"clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="high")
	left_credits=float((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	print "credits left= ",left_credits
    	assert_equal(left_credits,0.0)
	self.testHandler.handle_network_request("slab_disable")
	print "slab disabled"
	self.testHandler.handle_network_request("fd_disable")
	print " fd disabled"
	self.testHandler.handle_network_request("set_credit_limit:0",validity_level="medium")
	credit_limit=self.testHandler.handle_network_request("get_credit_limit")
	print "credit limit = ",credit_limit
    	print "setting price=100"
	self.testHandler.handle_network_request("set_price:100")
	time.sleep(1)
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])	
	print "price=",price
	self.testHandler.handle_network_request("recharge:25",validity_level="medium")
	print "recharged with 25"
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits",validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	print "accurate credits = ",acc_crdts
	a=float(acc_crdts)
	print "with 1 kw load and credit=25 with price =100 the credit should unniformly decrease to zero in 15 minutes"
	energy_initial=float((self.testHandler.handle_network_request("get_active_energy", validity_level="high")).split(" ")[0])	
	print "initial  energy =",energy_initial
	# load is 1 kw so 1 unit should be deduccted in 3600 seconds
	current_time =  str(self.testHandler.handle_network_request("get_time"))
	dt1= datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
	print "in date format ",dt1
	print "setting load"
	self.testHandler.handle_maxwell_request("voltage:100")
	self.testHandler.handle_maxwell_request("phase_load:10")
	time.sleep(5)
	#power cycle starts
        print'power cycle is starting'
	for i in range(5):
		self.testHandler.handle_maxwell_request("voltage:0")
        	time.sleep(1)
        	voltage_now=float((self.testHandler.handle_network_request("get_voltage", validity_level="medium")).split(" ")[0])
        	print "voltage= ",voltage_now
        	self.testHandler.handle_maxwell_request("voltage:100")
        	time.sleep(1)
        	voltage_now=float((self.testHandler.handle_network_request("get_voltage", validity_level="medium")).split(" ")[0])
        	print "voltage= ",voltage_now
        print'power cycle completed'
	# a is float value of credit in accurate credits
	while(a>0.0):
		
		power=float((self.testHandler.handle_network_request("get_active_power",validity_level="medium")).split(" ")[0])
		print "active power =",power," watts"
		acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
		acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
		print "accurate credits = ",acc_crdts
		a=float(acc_crdts)
	self.testHandler.handle_maxwell_request("voltage:0")
	energy_final=float((self.testHandler.handle_network_request("get_active_energy", validity_level="high")).split(" ")[0])	
	print "initial  energy =",energy_final	
	current_time =  str(self.testHandler.handle_network_request("get_time"))
	dt2= datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
	print "in date format ",dt2
	print('credits left should be zero now')
	print "credit left ==",a
	assert_equal(a,0.0)
	d3=(dt2-dt1)1
	print "time taken by the load to consume 25 cr @price=100 ",d3
	energy_consumed=(energy_final-energy_initial)
	print "energy consumed in this case = ",energy_consumed
    	#assert_between(energy_consumed,250,253)
	assert(250 <= energy_consumed <= 253)

    @attr(speed='pos')
    def test_03_credit_limit(self):
	"""
	TEST 3
	The test checks working of setting credit limit"""
	print "...starting test 2.03"
	print"clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="medium")
	left_credits=float((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	print "credits left= ",left_credits
    	assert_equal(left_credits,0.0)
	self.testHandler.handle_network_request("slab_disable")
	print "slab disabled"
	self.testHandler.handle_network_request("fd_disable")
	print " fd disabled"
	self.testHandler.handle_network_request("set_credit_limit:-10",validity_level="medium")
	credit_limit=self.testHandler.handle_network_request("get_credit_limit")
	print "credit limit = ",credit_limit
	print "setting price=100"
	self.testHandler.handle_network_request("set_price:100")
	time.sleep(1)
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])	
	print "price=",price
	print "with 1 kw load and credit=25 with price =100 the credit should unniformly decrease to zero in 15 minutes"
	# load is 1 kw so 1 unit should be deduccted in 3600 seconds
	self.testHandler.handle_network_request("recharge:25")
	time.sleep(2)
	print "recharging with 25"
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	#current_time =  str(self.testHandler.handle_network_request("get_time"))
	#print (current_time)
	self.testHandler.handle_maxwell_request("voltage:100")
	self.testHandler.handle_maxwell_request("phase_load:10")
	time.sleep(5)
	relay_stat=self.testHandler.handle_network_request("relay_state")
	#condition check for relay state( manual)
	print "starting for relay in manual control"
	self.testHandler.handle_network_request("relay_manual_control")
	relay_stat=self.testHandler.handle_network_request("relay_state")
	print "relay is in ",relay_stat	
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	while(a > -10.0):
		acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
		acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
		a=float(acc_crdts)
		print "accurate credits = ",a
		power=float((self.testHandler.handle_network_request("get_active_power",validity_level="medium")).split(" ")[0])
        	print "active power = ",power," watts"
		relay_stat=self.testHandler.handle_network_request("relay_state")
		print "relay is in ",relay_stat	
	assert_equal(a,-10.0)
	print "asserting manual control on"
	assert_equal(str(relay_stat),'MANUAL_CONTROL_ON')
	relay_stat=self.testHandler.handle_network_request("relay_state")
	print "relay is in ",relay_stat
	print "starting for relay in auto control resetting tamper latch make sure live cover open tamper is not there"
	print "recharging with 35  so that 35-10=25 should be the credit"
	time.sleep(2)
	self.testHandler.handle_network_request("reset_tamper_latch",validity_level="high")
	self.testHandler.handle_network_request("relay_auto_control",validity_level="high")
	time.sleep(2)
	self.testHandler.handle_network_request("recharge:35",validity_level="medium")
	time.sleep(2)
	self.testHandler.handle_network_request("reset_tamper_latch")
	time.sleep(2)
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	relay_stat=self.testHandler.handle_network_request("relay_state")
	print "relay is in ",relay_stat		
	print "after asserting for auto control on relay is in ",relay_stat	
	print "credit limit =", credit_limit
	assert_equal(str(relay_stat),'AUTO_CONTROL_ON')
	while(a > -10.0):
		power=float((self.testHandler.handle_network_request("get_active_power", validity_level="medium")).split(" ")[0])
        	print "active power = ",power," watts"
		relay_stat=self.testHandler.handle_network_request("relay_state")
		print "relay is in ",relay_stat
		acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
		acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
		a=float(acc_crdts)
		print "accurate credits = ",a
	assert_equal(a,-10.0)
	relay_stat=self.testHandler.handle_network_request("relay_state")
	print "relay is in ",relay_stat	
	print "relay status should be auto control off now AND CREDIT SHOULD NOT FALL BELOW -10 "
	assert_equal(str(relay_stat),'AUTO_CONTROL_OFF')
	relay_stat=self.testHandler.handle_network_request("relay_state")
	print "relay is in ",relay_stat
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	print"shifting relay to manual control on for further tests"
	self.testHandler.handle_network_request("relay_manual_control")
	self.testHandler.handle_network_request("turn_relay_on")
	relay_stat=self.testHandler.handle_network_request("relay_state")
	print "relay is in ",relay_stat'''


    @attr(speed='pos')
    def test_04_set_price(self):
	"""
	TEST 4
	The test checks if set price works properly"""
	print "...starting test 2.04"
	print "removing load"
	self.testHandler.handle_maxwell_request("voltage:0")
	self.testHandler.handle_maxwell_request("phase_load:10")
	time.sleep(5)
	power=float((self.testHandler.handle_network_request("get_active_power", validity_level="medium")).split(" ")[0])
        print "active power = ",power," watts"
	print"clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="high")
	time.sleep(2)	
	left_credits=float((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	print "credits left= ",left_credits
    	assert_equal(left_credits,0.0)
	self.testHandler.handle_network_request("slab_disable")
	print "slab disabled"
	self.testHandler.handle_network_request("fd_disable")
	print " fd disabled"
	self.testHandler.handle_network_request("set_credit_limit:0",validity_level="medium")
	credit_limit=self.testHandler.handle_network_request("get_credit_limit")
	print "credit limit = ",credit_limit
    	print "setting price=50"
	self.testHandler.handle_network_request("set_price:50")
	time.sleep(1)
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])	
	print "price=",price
	print "checking if price is equal to 50"
	assert_equal(price,50)
	print "setting price=70"
	self.testHandler.handle_network_request("set_price:70")
	time.sleep(1)
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])	
	print "price=",price
	print "checking if price is equal to 70"
	assert_equal(price,70)


    @attr(speed='pos')
    def test_05_credit_recharges(self):
        """
        TEST 5
        The test checks clearing of account ,recharge,fractional recharge,cummulative positive and cummulative recharges """
	print "...starting test 2.05 to 2.08 "
	print "removing load"
	self.testHandler.handle_maxwell_request("voltage:0")
	self.testHandler.handle_maxwell_request("phase_load:10")
	time.sleep(5)
	power=float((self.testHandler.handle_network_request("get_active_power", validity_level="medium")).split(" ")[0])
        print "active power = ",power," watts"	 
	self.testHandler.handle_network_request("clear_account", validity_level="high")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
   	assert_equal(a,0.0)
	print "recharging with 100"
	self.testHandler.handle_network_request("recharge:100", validity_level="medium")
	time.sleep(2)
	print ("recharge of 100 done  and starting the commulative recharge followed by fractional decharges")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	print"recharging with fractional recharge of .95"  
	self.testHandler.handle_network_request("recharge_fract:.95", validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	print"recharging with fractional recharge of .85"
	self.testHandler.handle_network_request("recharge_fract:.85", validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	print"recharging with a recharge of 100"
	self.testHandler.handle_network_request("recharge:100", validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits =",a
	print('commulattive positive recharge done \n starting commulative recharges')
	print"recharging with negative recharge of -50"
	self.testHandler.handle_network_request("recharge:-50", validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	print"recharging with negative recharge of -50"
	self.testHandler.handle_network_request("recharge:-50", validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	assert(101.79<a<=101.80)
    
    @attr(speed='pos')
    def test_06_allow_forbid_negative_recharges(self):
        """
        TEST 6
        The test checks allowing and forbidding recharges"""
	print "...starting test 2.09"
	self.testHandler.handle_maxwell_request("voltage:0")
	self.testHandler.handle_maxwell_request("phase_load:10")
	time.sleep(5)
	power=float((self.testHandler.handle_network_request("get_active_power", validity_level="medium")).split(" ")[0])
        print "active power = ",power," watts"
	self.testHandler.handle_network_request("set_credit_limit:-100")
	#test for allow or forbid negative recharges
	print"clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="high")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	assert_equal(a,0.0)
	print"allowing negative credits"
	self.testHandler.handle_network_request("allow_negative_credits")
	self.testHandler.handle_network_request("recharge:100")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	self.testHandler.handle_network_request("recharge:-120")
	time.sleep(2)
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	assert_equal(a,-20)
	print"test for forbid negative recharge strarted"
	print"clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="high")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	assert_equal(a,0.0)
	print"forbiding negative credits and recharging with 100"
	self.testHandler.handle_network_request("forbid_negative_credits")
	self.testHandler.handle_network_request("recharge:100")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	self.testHandler.handle_network_request("recharge:-120")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	assert(a!=-20.0)
	assert(a==100.0)
	print'it should not accept the recharge and then print credits'
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a


    @attr(speed='pos')
    def test_07_credit_deduction(self):
        """
        TEST 7
        The test checks if recharge positive but less than credit limit at minimum credit (at credit limit) to come above or equal to zero"""
	print "...starting test 2.07"
	print "clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="high")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a	
       	assert_equal(a,0.0)
       	self.testHandler.handle_network_request("set_credit_limit:-10")
	self.testHandler.handle_network_request("forbid_negative_credits")
	crd_limits=int((self.testHandler.handle_network_request("get_credit_limit", validity_level="medium")).split(" ")[0])
	print"printing credit limits after forbiding negative credits and putting on load"
	print "credit limit =",crd_limits
	self.testHandler.handle_maxwell_request("voltage:1000")
	self.testHandler.handle_maxwell_request("phase_load:100")
	power=float((self.testHandler.handle_network_request("get_active_power", validity_level="medium")).split(" ")[0])
        print "active power = ",power," watts"	
	while(a>-10.0):		
		power=float((self.testHandler.handle_network_request("get_active_power",validity_level="medium")).split(" ")[0])
		print "active power =",power," watts"
		acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
		acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
		a=float(acc_crdts)
		print "accurate credits = ",a
	assert_equal(a,-10.0)
	self.testHandler.handle_maxwell_request("voltage:0")
	self.testHandler.handle_maxwell_request("phase_load:10")
	time.sleep(1)
	power=float((self.testHandler.handle_network_request("get_active_power", validity_level="medium")).split(" ")[0])
        print "active power = ",power," watts"
	print('credits left should be -10')
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	print"recharging with negative recharge of 9"
	self.testHandler.handle_network_request("recharge:9")
	print"it should not accepct recharge so checking credits again"
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	print"now recharging with (11) value more than power limit ie..10"
	self.testHandler.handle_network_request("recharge:11", validity_level="medium")
	print"it should accepct recharge so checking credits again"
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	assert_equal(a,1.0)
	
    @attr(speed='pos')
    def test_08_credit_limit(self):
	"""
	TEST 8
	The test checks recharging beyond limits of variable(datatype) when negative credits are allowed"""
	print "...starting test 2.08"
	print "putting load off"
	self.testHandler.handle_maxwell_request("voltage:0")
	self.testHandler.handle_maxwell_request("phase_load:10")
	time.sleep(5)
	print"clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
    	assert_equal(a,0.0)
	self.testHandler.handle_network_request("slab_disable")
	print "slab disabled"
	self.testHandler.handle_network_request("fd_disable")
	print " fd disabled"
	self.testHandler.handle_network_request("set_credit_limit:-2147483648 ",validity_level="medium")
	credit_limit=int((self.testHandler.handle_network_request("get_credit_limit")).split(" ")[0])
	print "credit limit = ",credit_limit	
	print "recharging with 2147483647"
	self.testHandler.handle_network_request("recharge:2147483647")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	assert_equal(a,2147483647.0)
	print "recharging with 2"
	print "recharge should not be accepted and accurate credits should remain same"
	self.testHandler.handle_network_request("recharge:2")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	assert_equal(a,2147483647.0)
	print "starting test for negative limit"
	self.testHandler.handle_network_request("allow_negative_credits")
	print "permission for negative credits given"
	print"clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
    	assert_equal(a,0.0)	
	print "recharging with -2147483648"
	error=self.testHandler.handle_network_request("recharge:-2147483648",validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits after recharging with -2147483648= ",a
	assert_equal(a,-2147483648.0)
	print "recharging again with -2"
	print "recharge should not be accepted and accurate credits should remain same"
	self.testHandler.handle_network_request("recharge:-2")
	print" the credit shold not be accepted so credit should remain same"
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="medium")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	assert_equal(a,-2147483648.0) 

    @attr(speed='pos')
    def test_09_credit_limit(self):
	"""
	TEST 9 (it should fail for huge negative recharges)
	The test checks recharging beyond limits of variable(datatype) when negative credits are not allowed"""
	print "...starting test 2.09"
	print "putting load off"
	self.testHandler.handle_maxwell_request("voltage:0")
	self.testHandler.handle_maxwell_request("phase_load:10")
	time.sleep(5)
	self.testHandler.handle_network_request("forbid_negative_credits")
	print "restriction of negative credits"
	print"clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
    	assert_equal(a,0.0)
	print "recharging with 10"
	self.testHandler.handle_network_request("recharge:10")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	self.testHandler.handle_network_request("slab_disable")
	print "slab disabled"
	self.testHandler.handle_network_request("fd_disable")
	print " fd disabled"
	self.testHandler.handle_network_request("set_credit_limit:-2147483648 ",validity_level="medium")
	credit_limit=int((self.testHandler.handle_network_request("get_credit_limit")).split(" ")[0])
	print "credit limit = ",credit_limit	
	print"checking for huge positive recharge"
	print "recharging with 2147483660"
	self.testHandler.handle_network_request("recharge:2147483660",validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "recharge should not be accepted the ceredits should remain same "
	print "accurate credits = ",a
	assert_equal(a,10.0)
	print "passed for huge positive value test" 

	print "checking for huge negative values"
	print"clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
    	assert_equal(a,0.0)
	print "recharging with 10"
	self.testHandler.handle_network_request("recharge:10")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	print "recharging with -2147483660"
	self.testHandler.handle_network_request("recharge:-2147483660",validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "recharge should not be accepted the ceredits should remain same ie.. 10"
	print "accurate credits = ",a
	if(a>10.0):
		print "the value has got a jump towards positve end so test is about to fail"
	elif(a==10.0):
		print "the test should pass"
	else:
		print"the price has decreased from 10 check the load"
	assert_equal(a,10.0)
	
    
    @attr(speed='pos')
    def test_10_credit_limit(self):
	"""
	TEST 10 (it should fail)
	The test checks recharging beyond limits of variable(datatype)"""
	print "...starting test 2.10"
	print "putting load off"
	self.testHandler.handle_maxwell_request("voltage:0")
	self.testHandler.handle_maxwell_request("phase_load:10")
	time.sleep(5)
	self.testHandler.handle_network_request("allow_negative_credits")
	print "permission of negative credits"
	print"clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
    	assert_equal(a,0.0)
	print "recharging with 10"
	self.testHandler.handle_network_request("recharge:10")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	self.testHandler.handle_network_request("slab_disable")
	print "slab disabled"
	self.testHandler.handle_network_request("fd_disable")
	print " fd disabled"
	self.testHandler.handle_network_request("set_credit_limit:-2147483648 ",validity_level="medium")
	credit_limit=int((self.testHandler.handle_network_request("get_credit_limit")).split(" ")[0])
	print "credit limit = ",credit_limit	
	print"checking for huge positive recharge"
	print "recharging with 2147483660"
	self.testHandler.handle_network_request("recharge:2147483660",validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "recharge should not be accepted the ceredits should remain same "
	print "accurate credits = ",a
	if(a>10.0):
		print "the value has got a jump towards positve end so test is about to fail"
	elif(a==10.0):
		print "the test should pass"
	else:
		print"the price has jumped to huge negative value so test should fail"
	assert_equal(a,10.0)
	
    @attr(speed='pos')
    def test_11_credit_limit(self):
	"""
	TEST 11 (it should fail)
	The test checks recharging beyond limits of variable(datatype)"""
	print "...starting test 2.11"
	print "putting load off"
	self.testHandler.handle_maxwell_request("voltage:0")
	self.testHandler.handle_maxwell_request("phase_load:10")
	time.sleep(5)
	self.testHandler.handle_network_request("allow_negative_credits")
	print "permission of negative credits"
	print"clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
    	assert_equal(a,0.0)
	print "recharging with 10"
	self.testHandler.handle_network_request("recharge:10")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	self.testHandler.handle_network_request("slab_disable")
	print "slab disabled"
	self.testHandler.handle_network_request("fd_disable")
	print " fd disabled"
	self.testHandler.handle_network_request("set_credit_limit:-2147483648 ",validity_level="medium")
	credit_limit=int((self.testHandler.handle_network_request("get_credit_limit")).split(" ")[0])
	print "credit limit = ",credit_limit
	print "checking for huge negative values"
	print"clearing account"
	self.testHandler.handle_network_request("clear_account", validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
    	assert_equal(a,0.0)
	print "recharging with 10"
	self.testHandler.handle_network_request("recharge:10")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "accurate credits = ",a
	print "recharging with -2147483660"
	self.testHandler.handle_network_request("recharge:-2147483660",validity_level="medium")
	acc_crdts=self.testHandler.handle_network_request("get_accurate_credits", validity_level="high")
	acc_crdts= (acc_crdts.split("\n"))[3].split(" ")[2]
	a=float(acc_crdts)
	print "recharge should not be accepted the ceredits should remain same ie.. 10"
	print "accurate credits = ",a
	if(a>10.0):
		print "the value has got a jump towards positve end so test is about to fail"
	elif(a==10.0):
		print "the test should pass"
	else:
		print"the price has jumped to huge negative value so test should fail"
	assert_equal(a,10.0)
