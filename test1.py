tariff_dict = {1:{"no_of_slabs":4,
                                  "slab_limits":[30,50,100],
                                  "slab_prices":[1.70,2.10,2.40,2.80],
                                  "mmc":40,
                                  "meter_rent":10.0,
                                  "fixed_charges":0.0},

                   2:{"no_of_slabs":5,
                                  "slab_limits":[30,100,200,300],
                                  "slab_prices":[2.05,3.0,3.65,4.35,5.45],
                                  "mmc":50,
                                  "meter_rent":10.0,
                                  "fixed_charges":0.0},

                   3:{"no_of_slabs":3,
                                  "slab_limits":[50,100],
                                  "slab_prices":[2.1,2.4,2.8],
                                  "mmc":84,
                                  "meter_rent":20.0,
                                  "fixed_charges":0.0},

                   4:{"no_of_slabs":4,
                                  "slab_limits":[100,200,300],
                                  "slab_prices":[3.0,3.65,4.35,5.45],
                                  "mmc":0,
                                  "meter_rent":20.0,
                                  "fixed_charges":55.0},

                   5:{"no_of_slabs":1,
                                  "slab_limits":[1000],
                                  "slab_prices":[4.35],
                                  "mmc":174,
                                  "meter_rent":20.0,
                                  "fixed_charges":55.0},

                   6:{"no_of_slabs":3,
                                  "slab_limits":[100,200],
                                  "slab_prices":[2.40,2.80,3.20],
                                  "mmc":50,
                                  "meter_rent":20.0,
                                  "fixed_charges":0.0},

                   7:{"no_of_slabs":3,
                                  "slab_limits":[100,200],
                                  "slab_prices":[5.15,5.45,5.85],
                                  "mmc":257.5,
                                  "meter_rent":20.0,
                                  "fixed_charges":180.0},
                  }
x = 1

print('choose tariff among below given tariff plans')
print('press 1 for :tc_1')
print('press 2 for :tc_2')
print('press 3 for :tc_3')
print('press 4 for :tc_4')
print('press 5 for :tc_5')
print('press 6 for :tc_6')
print('press 7 for :tc_7')
print('please choose plan from 1 to 7')
while(x == 1):
    key = int(input('tariff category:'))
    add = int(input('meter address:'))
    print '2.2.0.' + str(add)
    credit=[]
    print tariff_dict[key]['no_of_slabs']
    for i in range (0,tariff_dict[key]['no_of_slabs'],1):
        credit.append(0)
    print 'deduction in different slabs initialized to zero:',credit
    kwh = int(input('consumed energy over a month'))
    kwhf=kwh
    print 'consumed units:', kwh
    a = tariff_dict[key]['no_of_slabs']

    if(len(tariff_dict[key]['slab_limits'])< 1):
        credit[0]= kwh * (tariff_dict[key]['slab_prices'][0])
        print 'credit under 1 slab:',credit[0]
        kwh = 0
        print 'remaining kwh:0'
        break 

    elif(kwh > tariff_dict[key]['slab_limits'][0]):
        print 'kwh is more than first slab'
        credit[0]= (tariff_dict[key]['slab_limits'][0]) * (tariff_dict[key]['slab_prices'][0])
        print 'credit under 1 slab:',credit[0]
        #kwh = kwh-tariff_dict['1']['slab_limits'][0]
        print 'remaining kwh:',kwh-tariff_dict[key]['slab_limits'][0]

    elif(kwh <= tariff_dict[key]['slab_limits'][0]):
        print 'kwh is less than first slab'
        credit[0]= kwh * (tariff_dict[key]['slab_prices'][0])
        print 'credit under 1 slab:',credit[0]
        kwh = 0
        print 'remaining kwh:0'



    



    
    for i in range(1,a-1,1):
        if(kwh >= tariff_dict[key]['slab_limits'][i] and (kwh > 0)):
            credit[i]= ((tariff_dict[key]['slab_limits'][i])-(tariff_dict[key]['slab_limits'][i-1])) * (tariff_dict[key]['slab_prices'][i])
            print 'credit under',i+1, ' slab:',credit[i]
            #kwh = kwh-tariff_dict['1']['slab_limits'][i]
            print 'remaining kwh:',kwh-tariff_dict[key]['slab_limits'][i]

        elif(kwh < tariff_dict[key]['slab_limits'][i] and (kwh > 0)):
            print 'kwh is less than ',i+1,'slab limit'
            kwh = kwh - tariff_dict[key]['slab_limits'][i-1]
            credit[i] = kwh * (tariff_dict[key]['slab_prices'][i])
            print 'credit under',i+1, ' slab:',credit[i]
            kwh=0
            print 'remaining kwh:0'
            

    if(kwh < tariff_dict[key]['slab_limits'][-1] and (kwh > 0) and len(tariff_dict[key]['slab_limits'])> 1):
            kwh = kwh - tariff_dict[key]['slab_limits'][-2]
            print 'kwh:',kwh
            credit[-1] = kwh * (tariff_dict[key]['slab_prices'][-2])
            print 'credit under last slab:',credit[-1]
            #kwh = kwh-tariff_dict['1']['slab_limits'][i]
            print 'remaining kwh:',kwh-tariff_dict[key]['slab_limits'][0]
            
    elif(kwh > tariff_dict[key]['slab_limits'][-1] and (kwh > 0) and len(tariff_dict[key]['slab_limits'])> 1):
            print 'elif2'
            kwh = kwh - tariff_dict[key]['slab_limits'][-1]
            print 'kwh:',kwh
            credit[-1] = kwh * (tariff_dict[key]['slab_prices'][-1])
            print 'credit under last slab:',credit[-1]
            #kwh = kwh-tariff_dict['1']['slab_limits'][i]
            print 'remaining kwh:0'
    
    print 'end'
    print 'credit:',credit
    energy_charge=0
    for i in range (0,tariff_dict[key]['no_of_slabs'],1):
        energy_charge = energy_charge + credit[i]
    energy_charge=energy_charge+(kwhf*(.10))
    print 'energy_charge(with rebet): ',str(energy_charge) + '\n'
    print 'energy_charge(after minus of rebet): ',str(energy_charge-(kwhf*(.10))) + '\n'
    if (energy_charge < tariff_dict[key]['mmc']):
        mmc1 = tariff_dict[key]['mmc']-energy_charge
        print 'mmc:',tariff_dict[key]['mmc']
        print 'at the end of month deducted amount:',mmc1
    else:
        mmc1=0
        print 'mmc deduction =',mmc1
    print 'FD=',tariff_dict[key]['fixed_charges']
    print 'Meter_rent=',tariff_dict[key]['meter_rent']
    print 'rebet=',(kwhf*(.10))
    bill_amount = (energy_charge+tariff_dict[key]['fixed_charges']+tariff_dict[key]['meter_rent'])
    print "total payable bill amount=",bill_amount
    bill_amount = 
