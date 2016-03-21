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

class TestSlab(object):
    
    @classmethod
    def setup_class(self):
        print "Slab APP Tests"
	#self.test_handler = RequestHandler()        
	self.testHandler = RequestHandler()
        self.testHandler.handle_network_request("set_power_limit:70000000")
        
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

    @attr(speed='pos')
    def test_01_reset_slab(self):
         """
         TEST1 : The test checks the resetting the slab.
         """
	 #f = open('/home/grampower/reports/v1_3.xls','a+')	
	 f.write('TEST1 : The test checks the resetting the slab'+'\n')
         self.testHandler.handle_network_request("slab_reset",validity_level="high")
         asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
         print asp
	 #f.write(str(asp.split("\n"))[6])+'\n')
	 asp = (asp.split("\n"))[6].split(":")[1]
         assert_equal(int(asp),0)

    @attr(speed='pos')
    def test_02_slab_deduction(self):
        """
        TEST2
        The test checks the resetting the slab,then sets the update time and sees whether the
        slab set is updated.The time period taken into account is within the same month.
        """
	print "...starting test 02"
        
        #change_time = datetime.datetime(2016, 01, 01, 10, 30, 15)
        #set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request("time now")
        time.sleep(12)
	get_time = self.testHandler.handle_network_request("get_time", validity_level="high")
	print "get_time:",get_time		

	self.testHandler.handle_network_request("slab_reset")        
	self.testHandler.handle_network_request("set_slab_params:3,[10000,30000,45000,0,0,0],[4,8,0,0,0],5500", validity_level="high")
        self.testHandler.handle_network_request("set_slab_update_ts:now+5", validity_level="high")
        self.testHandler.handle_network_request("slab_enable", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")
        time.sleep(10)
        self.testHandler.handle_network_request("recharge:50")
       	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
	print asp
	self.testHandler.handle_maxwell_request("voltage:200")        
	self.testHandler.handle_maxwell_request("phase_load:1")
	time.sleep(2)
	print "active_power", self.testHandler.handle_network_request("get_active_power", validity_level="medium")        
        time.sleep(38)
        self.testHandler.handle_maxwell_request("phase_load:1000000000")
        left_credits=int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
        #time.sleep(2)
        consumed_energy=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
        #cal_credits = (4)+(12)+(((consumed_energy/1000) - 8)*4.5)
        print "consumed_energy:",consumed_energy
        print str(left_credits)
        assert(left_credits > 0) 
	assert(left_credits < 2)



    @attr(speed='pos')
    def test_03_deduction_over_month_transition(self):
        """
        TEST3
        This test verifies the credit deduction over the month boundary
        """
	print "...starting test 03"
        change_time = datetime.datetime(2015, 07, 31, 10, 30, 41)
	set_time = '{}:{}'.format('time',str(change_time))
	self.testHandler.handle_maxwell_request(set_time)
	time.sleep(10)
	#self.testHandler.handle_maxwell_request("time 2015-01-01 00:09:00")
        #time.sleep(12)
	get_time = self.testHandler.handle_network_request("get_time", validity_level="high")
	print "get_time:",get_time		

	self.testHandler.handle_network_request("slab_reset")        
	self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[4,8,0,0,0],0", validity_level="high")
        self.testHandler.handle_network_request("set_slab_update_ts:2015-07-31 10:31:15", validity_level="high")
        self.testHandler.handle_network_request("slab_enable", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")
        time.sleep(10)
	print "get_time:", self.testHandler.handle_network_request("get_time")
        time.sleep(1)
	print "update_ts:", self.testHandler.handle_network_request("get_slab_update_ts")
        self.testHandler.handle_network_request("recharge:50")
	self.testHandler.handle_network_request("allow_negative_credits")
       	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
	print "accounting_state:", asp

        self.testHandler.handle_maxwell_request("phase_load:1")
        self.testHandler.handle_maxwell_request("voltage:1000")
        time.sleep(20)
        self.testHandler.handle_maxwell_request("phase_load:1000000000")
        consumed_energy_m1=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])

        change_time = datetime.datetime(2015, 8, 01, 10, 30, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(8)

        self.testHandler.handle_maxwell_request("phase_load:1") 
        time.sleep(20)
	self.testHandler.handle_maxwell_request("phase_load:1000000")
        consumed_energy_m2=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
        print "consumed_energy_01:",str(consumed_energy_m1)
        print "consumed_energy_02:",str(consumed_energy_m2)
        cal_credits = (4)+(((consumed_energy_m1/1000.0) - 4.0)*3.0) + (4.0)+((((consumed_energy_m2 - consumed_energy_m1)/1000.0) - 4.0)*3.0)
        left_credits=int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
        print "expected_deduction:",str(cal_credits)
        print "actual_deduction:",str(50-left_credits)
        assert (cal_credits - (50-left_credits)) < 4 



    @attr(speed='pos')
    def test_04_only_mmc_dedcution(self):
        """
        TEST4
        This test verifies the credit deduction over the month boundary(for MMC in case of zero energy usage)
        """
	print "...starting test 04 to test mmc deduction over month transistion"
        change_time = datetime.datetime(2016, 02, 01, 10, 30, 41)
	set_time = '{}:{}'.format('time',str(change_time))
	self.testHandler.handle_maxwell_request(set_time)
	time.sleep(10)
	#current_time =  str(self.testHandler.handle_network_request("get_time").split(" ")[0])
	#assert_equal(current_time,"2016-02-01")
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:3,[200,300,450,0,0,0],[4,10,0,0,0],4000", validity_level="medium")
	self.testHandler.handle_network_request("set_slab_update_ts:2016-02-01 10:31:15", validity_level="high")        
	self.testHandler.handle_network_request("slab_enable", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")
        time.sleep(1)
        self.testHandler.handle_network_request("recharge:50")
       	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
	print "accounting_state:", asp
        change_time = datetime.datetime(2016, 02, 29, 23, 59, 50)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(15)
        credits_left = int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
        assert_equal(credits_left,10)


    @attr(speed='pos')
    def test_05_deduction_with_maxslabs_according_slab(self):
        """
        TEST5
        This test verifies the credit deduction over the month according to slab prices and slab limits,no MMC deduction case test
        """
	print "...starting test 05 This test verifies the credit deduction over the month according to slab prices and slab limits,no MMC deduction case tes"
        change_time = datetime.datetime(2016, 01, 01, 00, 00, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(10)
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:6,[100,300,450,600,700,900],[1,2,3,5,10],4500", validity_level="medium")
	current_time =  str(self.testHandler.handle_network_request("get_time"))
	print "get_time:",current_time
        self.testHandler.handle_network_request("set_slab_update_ts:2016-01-01 00:00:36", validity_level="high")
        time.sleep(1)        
	self.testHandler.handle_network_request("slab_enable", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")

        self.testHandler.handle_network_request("recharge:100")
	consumed_energy_m1=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
       	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
	print "accounting_state:", asp

        self.testHandler.handle_maxwell_request("voltage:1000")
	self.testHandler.handle_maxwell_request("phase_load:1")
	        
	time.sleep(39)
	#price=self.testHandler.handle_network_request("get_price")
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])	
	#print price
        self.testHandler.handle_maxwell_request("phase_load:1000000000")

        change_time = datetime.datetime(2016, 01, 31, 23, 59, 50)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(10)
        #self.testHandler.handle_maxwell_request("phase_load:1") 
        #time.sleep(20)
        consumed_energy_m2=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
        print "consumed_energy_m1:",str(consumed_energy_m1)
        print "consumed_energy_m2:",str(consumed_energy_m2)
        left_credits=int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
        #print str(cal_credits)
        print "left_credits:",str(left_credits)
	assert(left_credits < 30)		
        assert(left_credits > 28) 	
	assert_equal(price,9.0)
        

    @attr(speed='pos')
    def test_06_deduction_with_maxslabs_according_slab(self):
        """
        TEST6
        This test verifies the credit deduction over the month according to slab prices and slab limits,MMC deduction case test
        """
	print "...starting test 06 This test verifies the credit deduction over the month according to slab prices and slab limits, MMC deduction case tes"
        change_time = datetime.datetime(2016, 01, 01, 00, 00, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(10)
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:6,[100,300,450,600,700,900],[1,2,3,5,10],7500", validity_level="medium")
	current_time =  str(self.testHandler.handle_network_request("get_time"))
	print (current_time)
        self.testHandler.handle_network_request("set_slab_update_ts:2016-01-01 00:00:36", validity_level="high")
        time.sleep(1)        
	self.testHandler.handle_network_request("slab_enable", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")

        self.testHandler.handle_network_request("recharge:100")
	consumed_energy_m1=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
       	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
	print "accounting_state:", asp

        self.testHandler.handle_maxwell_request("voltage:1000")
	self.testHandler.handle_maxwell_request("phase_load:1")
	        
	time.sleep(39)
	#price=self.testHandler.handle_network_request("get_price")
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])	
	#print price
        self.testHandler.handle_maxwell_request("phase_load:1000000000")

        change_time = datetime.datetime(2016, 01, 31, 23, 59, 50)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(10)
        #self.testHandler.handle_maxwell_request("phase_load:1") 
        #time.sleep(20)
        consumed_energy_m2=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
        print str(consumed_energy_m1)
        print str(consumed_energy_m2)
        left_credits=int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
        #print str(cal_credits)
        print str(left_credits)
	assert_equal(left_credits,25)		
        #assert(left_credits > 28) 	
	assert_equal(price,9.0)


    @attr(speed='pos')
    def test_07_reset_update_slab(self):
        """
        TEST7
        The test checks the activation of slab params just after update_ts crossing along with its state.this first test checks whether after resetting slab , slab is disabled or not. then after defining new slab params and their update_ts crossed by meter RTC. whether Slab is enabled or not. and in last checking price of slab. whether price is of first slab or random.
        """
	print "...starting test 07 to check activation of slab params"       
        self.testHandler.handle_maxwell_request("time:2015-07-07 10:30:15")
	time.sleep(6)	
	self.testHandler.handle_network_request("slab_reset", validity_level="high")	
	self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[20,30,0,0,0],9000", validity_level="high")        
        self.testHandler.handle_network_request("set_slab_update_ts:2015-07-07 10:30:45")
	#get_time = self.test_handler.handle_network_request("get_time",3)
	#print get_time		
	
	time.sleep(5)
        asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
	print asp
        asp1 = (asp.split("\n"))[6].split(":")[1]
	asp2 = (asp.split("\n"))[7].split(":")[1]
	print asp1
	print asp2
        assert_equal(int(asp1),0)
	assert_equal(int(asp2),2)
        time.sleep(12) 
	
	self.testHandler.handle_network_request("slab_enable", validity_level="high")         
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        asp1 = (asp.split("\n"))[6].split(":")[1]
	asp2 = (asp.split("\n"))[7].split(":")[1]
        assert_equal(int(asp1),1)
	assert_equal(int(asp2),1)
        price=float(self.testHandler.handle_network_request("get_price", validity_level="high").split(" ")[0])
	print price	
	assert_equal(price,1.0)
	print "finish test 07"


    @attr(speed='pos')
    def test_08_deduction_over_month_transition(self):
        """
        TEST8 : This test verifies the credit deduction over the month boundary
        """
	print "...This test verifies the credit deduction over the month boundary"        
	change_time = datetime.datetime(2015, 07, 31, 10, 30, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(15)
	#get_time = self.test_handler.handle_network_request("get_time",3)
	#print get_time
        #self.testHandler.handle_network_request("reset",exception_handling=False)
        #time.sleep(5)

        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[4,8,0,0,0],0", validity_level="medium")
 	self.testHandler.handle_network_request("set_slab_update_ts:2015-07-31 10:30:20", validity_level="high")       
	self.testHandler.handle_network_request("slab_enable", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")


        self.testHandler.handle_network_request("set_slab_update_ts:2015-07-31 10:30:45", validity_level="high")
        time.sleep(1)
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp
	consumed_energy_m0=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])        
	self.testHandler.handle_network_request("recharge:50",exception_handling=True)
        self.testHandler.handle_maxwell_request("phase_load:1")
        self.testHandler.handle_maxwell_request("voltage:1000")
        time.sleep(20)
        self.testHandler.handle_maxwell_request("phase_load:1000000000")
        consumed_energy_m1=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
	left_credits_1=int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	print str(left_credits_1)
        change_time = datetime.datetime(2015, 8, 01, 10, 30, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(15)
        print (cal_credits - (50-left_credits_3))
        self.testHandler.handle_maxwell_request("phase_load:1") 
        time.sleep(20)
	self.testHandler.handle_maxwell_request("phase_load:10000000") 
        	
	left_credits_2=int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	print str(left_credits_2)
        consumed_energy_m2=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
	print str(consumed_energy_m0)        
	print str(consumed_energy_m1)
        print str(consumed_energy_m2)
        cal_credits = (4)+(((consumed_energy_m1/1000.0) - 4.0)*3.0) + (4.0)+((((consumed_energy_m2 - consumed_energy_m1)/1000.0) - 4.0)*3.0)
        left_credits_3=int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
        print str(cal_credits)
        print str(left_credits_3)
	diff = cal_credits - (50-left_credits_3)
        print (cal_credits - (50-left_credits_3))
        assert_equal(int(diff),0)



    @attr(speed='pos')
    def test_09_slab_transistion_over_month_transition(self):
        """
        TEST9
        This test verifies the slab update on particular time functionality.
        """
	print "...starting test 09 This test verifies the slab update on particular time functionality"
        change_time = datetime.datetime(2016, 01, 01, 00, 00, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(8)
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[4,8,0,0,0],0", validity_level="medium")
	self.testHandler.handle_network_request("set_slab_update_ts:2016-01-01 00:00:29", validity_level="high")        
	self.testHandler.handle_network_request("slab_enable", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")
        
	self.testHandler.handle_network_request("set_slab_params:6,[900,800,700,600,500,400],[1,2,3,4,5],0", validity_level="medium")
        self.testHandler.handle_network_request("set_slab_update_ts:2016-02-01 00:00:00", validity_level="high")
	time.sleep(1)
        self.testHandler.handle_network_request("recharge:100")
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp

        self.testHandler.handle_maxwell_request("phase_load:1")
        self.testHandler.handle_maxwell_request("voltage:1000")
        time.sleep(20)
        self.testHandler.handle_maxwell_request("phase_load:1000000000")
        consumed_energy_m1=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
	price_1=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])
	print price_1


        change_time = datetime.datetime(2016, 01, 31, 23, 59, 50)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(15)
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp

        self.testHandler.handle_maxwell_request("phase_load:1") 
        time.sleep(20)
	self.testHandler.handle_maxwell_request("phase_load:999999")
        consumed_energy_m2=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
        print str(consumed_energy_m1)
        print str(consumed_energy_m2)
        cal_credits = int((4)+(((consumed_energy_m1/1000.0) - 4.0)*3.0) + (35.0)+((((consumed_energy_m2 - consumed_energy_m1)/1000.0) - 5.0)*4.0))
	print int((4.0)+(((consumed_energy_m1/1000.0) - 4.0)*3.0))
	print int((35.0)+((((consumed_energy_m2 - consumed_energy_m1)/1000.0) - 5.0)*4.0))
	print cal_credits
        left_credits=int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
      	print left_credits
	credit_consumed = 100 - left_credits
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])
	print price
	assert_equal(price,4.0)
	assert_equal(price_1,3.0)
	assert(credit_consumed < (cal_credits+4 ))
	assert(credit_consumed > (cal_credits-4))
	

    @attr(speed='pos')
    def test_10_slab_transistion_in_same_month(self):
        """
        TEST10
        This test verifies the slab update on particular time functionality within month(Two SlaBS in one Month)
        """
	print "...starting test 10 This test verifies the slab update on particular time functionality within month(Two SlaBS in one Month)"
        change_time = datetime.datetime(2016, 01, 01, 00, 00, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(8)
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[4,8,0,0,0],0", validity_level="medium")
	self.testHandler.handle_network_request("set_slab_update_ts:2016-01-01 00:00:32", validity_level="high")       
	self.testHandler.handle_network_request("slab_enable", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        
	self.testHandler.handle_network_request("set_slab_params:6,[900,800,700,600,500,400],[1,2,3,4,5],0", validity_level="medium")
        self.testHandler.handle_network_request("set_slab_update_ts:2016-01-15 00:00:00", validity_level="high")
	time.sleep(1)
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp

        self.testHandler.handle_network_request("recharge:100")
        price_1=float((self.testHandler.handle_network_request("get_price", validity_level="medium")).split(" ")[0])
	print price_1
        change_time = datetime.datetime(2016, 01, 14, 23, 59, 52)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(12)
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp

        price_2=float((self.testHandler.handle_network_request("get_price", validity_level="medium")).split(" ")[0])
	print price_2
        left_credits=int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
        credit_consumed = 100 - left_credits
	assert_equal(price_1,1.0)
	assert_equal(price_2,9.0)
	assert_equal(credit_consumed,0)


    @attr(speed='pos')
    def test_11_MMC_more_than_available_credits(self):
        """
        TEST11
        this test case will check app behave when credits available are less than MMC amount to be deducted along with it, this test will check credit deduction in negative side as well
        """
	print "...starting test 11 this test case will check app behave when credits available are less than MMC amount to be deducted along with it, this test will check credit deduction in negative side as well"
        change_time = datetime.datetime(2016, 01, 01, 00, 00, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(8)
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[4,8,0,0,0],7500", validity_level="medium")
	self.testHandler.handle_network_request("set_slab_update_ts:2016-01-01 00:00:35", validity_level="high")       
        self.testHandler.handle_network_request("slab_enable", validity_level="medium")
	self.testHandler.handle_network_request("set_credit_limit:-100", validity_level="medium")		
	self.testHandler.handle_network_request("allow_negative_credits", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp
       
        self.testHandler.handle_network_request("recharge:50")
        change_time = datetime.datetime(2016, 01, 31, 23, 59, 52)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(12)
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        balance = int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	print "credits",balance
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])
	print price
	assert_equal(price,1.0)
	assert_equal(balance,-25)
	consumed_energy_m1=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
	print "energy_m1", consumed_energy_m1
	self.testHandler.handle_maxwell_request("phase_load:1")
        self.testHandler.handle_maxwell_request("voltage:1000")
        time.sleep(20)			
	self.testHandler.handle_maxwell_request("phase_load:10000000")
        consumed_energy_m2=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
	consumed_energy = consumed_energy_m2 - consumed_energy_m2
	print "energy_m2", consumed_energy_m2
	balance_1 = int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	assert_equal(balance_1,-35)





    @attr(speed='neg')
    def test_12_credit_deduction_in_negative_side_after_crossing_credit_limit(self):
        """
        TEST12
        if credit limit is less value and relay manually ON meter have less credits than MMC and say energy usage(to check credit deduction continuety after credit limit)
        """
	print "...starting test 12  if credit limit is less value and relay manually ON meter have less credits than MMC and say energy usage(to check credit deduction continuety after credit limit)"
        change_time = datetime.datetime(2016, 01, 01, 00, 00, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(8)
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[4,8,0,0,0],7500", validity_level="medium")
	self.testHandler.handle_network_request("set_slab_update_ts:2016-01-01 00:00:35", validity_level="high")       
        self.testHandler.handle_network_request("slab_enable", validity_level="medium")
	self.testHandler.handle_network_request("set_credit_limit:-25", validity_level="medium")
	self.testHandler.handle_network_request("relay_auto_control", validity_level="medium")
			
	self.testHandler.handle_network_request("allow_negative_credits", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp
       
        self.testHandler.handle_network_request("recharge:50")
        change_time = datetime.datetime(2016, 01, 31, 23, 59, 52)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(12)
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        balance = int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	print "credits",balance
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])
	print price
	assert_equal(price,1.0)
	assert_equal(balance,-25)
	consumed_energy_m1=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
	print "energy_m1", consumed_energy_m1
	self.testHandler.handle_maxwell_request("phase_load:1")
        self.testHandler.handle_maxwell_request("voltage:1000")
        time.sleep(20)			
	self.testHandler.handle_maxwell_request("phase_load:10000000")
        consumed_energy_m2=int((self.testHandler.handle_network_request("get_active_energy", validity_level="medium")).split(" ")[0])
	consumed_energy = consumed_energy_m2 - consumed_energy_m2
	print "energy_m2", consumed_energy_m2
	balance_1 = int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	print balance_1	
	print "this is negative type case so it will fail "	
	assert_equal(balance_1,-35)


       

    @attr(speed='pos')
    def test_13_slab_in_leap_year(self):
        """
        TEST13
        to check whether slab is working correct or not in feb to march transistion of leap year
        """
	print "...starting test 13 to check whether slab is working correct or not in feb to march transistion of leap year"
        change_time = datetime.datetime(2016, 02, 05, 00, 00, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(15)
	self.testHandler.handle_network_request("fd_disable")
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[4,8,0,0,0],7500", validity_level="medium")
	self.testHandler.handle_network_request("set_slab_update_ts:2016-02-05 00:00:44", validity_level="high")       
        self.testHandler.handle_network_request("slab_enable", validity_level="medium")
	print self.testHandler.handle_network_request("get_time", validity_level="high") 
	#self.testHandler.handle_network_request("slab_enable", validity_level="medium")		
	self.testHandler.handle_network_request("allow_negative_credits", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")
        self.testHandler.handle_network_request("recharge:50")
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp

        change_time = datetime.datetime(2016, 03, 20, 23, 59, 52)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(12)
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        balance = int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])
	assert_equal(price,1.0)
	assert_equal(balance,-25)


    @attr(speed='pos')
    def test_14_slab_in_non_leap_year(self):
        """
        TEST14
        to check whether slab is working correct or not in feb to march transistion of non leap year
        """
	print "...starting test 14 to check whether slab is working correct or not in feb to march transistion of non leap year"
        change_time = datetime.datetime(2017, 02, 01, 00, 00, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(8)
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[4,8,0,0,0],7500", validity_level="medium")
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        self.testHandler.handle_network_request("set_slab_update_ts:2017-02-01 00:00:32", validity_level="high")
        self.testHandler.handle_network_request("slab_enable", validity_level="medium")		
	self.testHandler.handle_network_request("allow_negative_credits", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")



        self.testHandler.handle_network_request("recharge:50")
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp

        change_time = datetime.datetime(2017, 02, 28, 23, 59, 52)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(15)
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        balance = int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])
	assert_equal(price,1.0)
	assert_equal(balance,-25)




    @attr(speed='pos')
    def test_15_mmc_deduction_for_non_power_month(self):
        """
        TEST15
        to check whether mmc is deducting for no-power month.
	time will directly reach to  may from feb . 
        """
	print "...starting test 15 to check whether mmc is deducting for no-power month. time will directly reach to  may from feb ."
        change_time = datetime.datetime(2016, 02, 01, 00, 00, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(8)
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[4,8,0,0,0],7500", validity_level="medium")
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        self.testHandler.handle_network_request("set_slab_update_ts:2016-02-01 00:00:38", validity_level="high")
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        self.testHandler.handle_network_request("slab_enable", validity_level="medium")		
	self.testHandler.handle_network_request("allow_negative_credits", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")
        self.testHandler.handle_network_request("recharge:50")
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp
        change_time = datetime.datetime(2016, 04, 30, 23, 59, 52)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(12)
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        balance = int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])
	assert_equal(price,1.0)
	assert_equal(balance,-175)



       

    @attr(speed='neg')
    def test_16_slab_in_leap_year(self):
        """
        TEST16
        to check whether slab is working correct or not in Jan  to next year's Jan transistion of leap year
        """
	print "...starting test 16 to check whether slab is working correct or not in  leap year's Jan  to next year's Jan transistion of leap year"
        change_time = datetime.datetime(2016, 01, 01, 00, 00, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(15)
	self.testHandler.handle_network_request("fd_disable")
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[4,8,0,0,0],7500", validity_level="medium")
	self.testHandler.handle_network_request("set_slab_update_ts:2016-01-01 00:00:44", validity_level="high")       
        self.testHandler.handle_network_request("slab_enable", validity_level="medium")
	print self.testHandler.handle_network_request("get_time", validity_level="high") 
	#self.testHandler.handle_network_request("slab_enable", validity_level="medium")		
	self.testHandler.handle_network_request("allow_negative_credits", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")
        self.testHandler.handle_network_request("recharge:1000")
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp

        change_time = datetime.datetime(2017, 01, 01, 23, 59, 52)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(15)
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        balance = int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])
	assert_equal(price,1.0)
	assert_equal(balance,100)


    @attr(speed='neg')
    def test_17_slab_in_non_leap_year(self):
        """
        TEST17
        to check whether slab is working correct or not in non leap year's Jan to Jan of leap year transistion of non leap year
        """
	print "...starting test 17 to check whether slab is working correct or not in non leap year's Jan to Jan of leap year transistion of non leap year"
        change_time = datetime.datetime(2019, 01, 01, 00, 00, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(8)
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[4,8,0,0,0],7500", validity_level="medium")
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        self.testHandler.handle_network_request("set_slab_update_ts:2019-01-01 00:00:44", validity_level="high")
        self.testHandler.handle_network_request("slab_enable", validity_level="medium")		
	self.testHandler.handle_network_request("allow_negative_credits", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")

	time.sleep(2)

        self.testHandler.handle_network_request("recharge:1000")
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp

        change_time = datetime.datetime(2020, 01, 01, 23, 59, 52)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(15)
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        balance = int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])
	assert_equal(price,1.0)
	assert_equal(balance,100)

       

    @attr(speed='pos')
    def test_18_slab_in_leap_year(self):
        """
        TEST18
        to check whether slab is working correct or not in Jan  to next year's Jan transistion of leap year
        """
	print "...starting test 18 to check whether slab is working correct or not in  leap year's Jan  to next year's dec and jan. transistion of leap year"
        change_time = datetime.datetime(2016, 01, 01, 00, 00, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(15)
	self.testHandler.handle_network_request("fd_disable")
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[4,8,0,0,0],7500", validity_level="medium")
	self.testHandler.handle_network_request("set_slab_update_ts:2016-01-01 00:00:44", validity_level="high")       
        self.testHandler.handle_network_request("slab_enable", validity_level="medium")
	print self.testHandler.handle_network_request("get_time", validity_level="high") 
	#self.testHandler.handle_network_request("slab_enable", validity_level="medium")		
	self.testHandler.handle_network_request("allow_negative_credits", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")
        self.testHandler.handle_network_request("recharge:1000")
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp

        change_time = datetime.datetime(2016, 12, 31, 23, 59, 52)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(15)
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        balance = int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])
	assert_equal(price,1.0)
	assert_equal(balance,100)


    @attr(speed='pos')
    def test_19_slab_in_non_leap_year(self):
        """
        TEST19
        to check whether slab is working correct or not in non leap year's Jan to Jan of leap year transistion of non leap year
        """
	print "...starting test 19 to check whether slab is working correct or not in non leap year's Jan to dec and then jan transistion of non leap year"
        change_time = datetime.datetime(2019, 01, 01, 00, 00, 15)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(8)
        self.testHandler.handle_network_request("slab_reset")
        self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,0,0,0],[4,8,0,0,0],7500", validity_level="medium")
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        self.testHandler.handle_network_request("set_slab_update_ts:2019-01-01 00:00:44", validity_level="high")
        self.testHandler.handle_network_request("slab_enable", validity_level="medium")		
	self.testHandler.handle_network_request("allow_negative_credits", validity_level="medium")
        self.testHandler.handle_network_request("clear_account", validity_level="medium")

	time.sleep(2)

        self.testHandler.handle_network_request("recharge:1000")
	asp = self.testHandler.handle_network_request("get_accounting_state", validity_level="high")
        print asp

        change_time = datetime.datetime(2019, 12, 31, 23, 59, 52)
        set_time = '{}:{}'.format('time',str(change_time))
        self.testHandler.handle_maxwell_request(set_time)
        time.sleep(15)
	print self.testHandler.handle_network_request("get_time", validity_level="high")
        balance = int((self.testHandler.handle_network_request("get_credits", validity_level="medium")).split(" ")[0])
	price=float((self.testHandler.handle_network_request("get_price", validity_level="high")).split(" ")[0])
	assert_equal(price,1.0)
	assert_equal(balance,100)




    @attr(speed='neg')
    def test_20_exception_handling_for_incorrect_argument_passing(self):
        """
        TEST20
        This test verifies the exception handeling for incoreect slab params setting
        """
	print "...starting test 20  This test verifies the exception handeling for incoreect slab params setting"

        result_1 = self.testHandler.handle_network_request("set_slab_params:6,[100,300,450,600,700,900],[1,2,3,5,10],0", validity_level="medium")
	result_2 = self.testHandler.handle_network_request("set_slab_params:8,[100,300,450,600,700,900],[1,2,3,5,10],0", validity_level="medium")
	result_3 = self.testHandler.handle_network_request("set_slab_params:3,[100,300,450,600,700,900],[1,2,3,5,10],0", validity_level="medium")
	#result_4 = self.testHandler.handle_network_request("set_slab_params:6,[100,300,450,600,700,900,900],[1,2,3,5,10],0", validity_level="medium")
	#result_5 = self.testHandler.handle_network_request("set_slab_params:6,[100,300,450,600,700,900],[1,2,3,5,10,78],0", validity_level="medium")
	result_6 = self.testHandler.handle_network_request("set_slab_params:6,[100,300,450,600,700,900],[1,2,3,5,10],65534", validity_level="medium")
	#result_7 = self.testHandler.handle_network_request("set_slab_params:6,[100,65537,450,600,700,900],[1,2,3,5,10],0", validity_level="medium")
	result_8 = self.testHandler.handle_network_request("set_slab_params:6,[100,300,450,600,700,900],[1,65535,3,5,10],0", validity_level="medium")
	result_9 = self.testHandler.handle_network_request("set_slab_params:6,[100,300,450,600,700,900],[1,5,3,6,10],0", validity_level="medium")
	print "checking reply for set_slab_params:6,[100,300,450,600,700,900],[1,2,3,5,10],0" 	
	print result_1	
	assert_equal(result_1,"ok")
	
	print "checking reply for set_slab_params:8,[100,300,450,600,700,900],[1,2,3,5,10],0" 	
	print result_2	
	#assert_not_equal(result_2,"ok")
	print "checking reply for set_slab_params:3,[100,300,450,600,700,900],[1,2,3,5,10],0" 	
	print result_3	
	#assert_not_equal(result_3,"ok")
	#print "checking reply for set_slab_params:6,[100,300,450,600,700,900,900],[1,2,3,5,10],0" 	
	#print result_4	
	#assert_not_equal(result_4,"ok")
	#print "checking reply for set_slab_params:6,[100,300,450,600,700,900],[1,2,3,5,10,78],0" 	
	#print result_5	
	#assert_not_equal(result_5,"ok")
	print "checking reply for set_slab_params:6,[100,300,450,600,700,900],[1,2,3,5,10],65534" 	
	print result_6	
	assert_equal(result_6,"ok")
	#print "checking reply for set_slab_params:6,[100,65537,450,600,700,900],[1,2,3,5,10],0" 	
	#print result_7	
	#assert_not_equal(result_2,"ok")
	print "checking reply for set_slab_params:6,[100,300,450,600,700,900],[1,65535,3,5,10],0" 	
	print result_8	
	assert_not_equal(result_2,"ok")
	print "checking reply for set_slab_params:6,[100,300,450,600,700,900],[1,5,3,6,10],0" 	
	print result_9	
	assert_not_equal(result_2,"ok")


