from rspngparser import get_valuable_drop_strings
import time
import os
import shutil
import uuid

webpage = '''
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="1">
<link rel="stylesheet" href="styles.css">
</head>
<body>

<progress max="1000000000" value="%d" text="%sm (Total)"></progress>

<br><br>
<progress max="13000000" value="%d" text="%sm (Day)"></progress>
<body>
'''

daily_total = float(5000000)
loot_track_dir = "C:\\Users\\username\\osrs_loot_tracker\\"
webpage_dir = loot_track_dir+"loottrack\\progress.html"

screenshot_dir = "C:\\Users\\username\\OneDrive\\Pictures\\Screenshots"
used_screenshot_dir = loot_track_dir+"UsedScreenshots"
total_loot_dir = loot_track_dir+"total_loot.txt"
alltime_loot_dir = loot_track_dir+"alltime_loot.txt"
hundredpercent_loot = loot_track_dir+"100percent_loot.txt"
manual_adjustment = loot_track_dir+"manual_adjustment.txt"
coins_file = loot_track_dir+"coins.txt"

def parse_val_strings(string_list):
    total_value = 0
    if string_list == None:
        return total_value
    while(string_list != []):
        loot_string = string_list.pop()
        #print loot_string
        if "Valuable drop" not in loot_string:
            total_value+=0
        else:

            try:                
                num_start = loot_string[::-1].find("(")+1
                num_start = len(loot_string)-num_start+1
                #raw_input(str(num_start))
                
                num_end = loot_string[num_start:].find(" coins")
                #raw_input(str(num_end))
                
                #raw_input(str(loot_string[num_start:][:num_end]))
                num = int(loot_string[num_start:][:num_end])
                #print num
                total_value += num
                if "Coins" in loot_string:
                    print "Adding coins to coins file"
                    f = open(coins_file, "rb")
                    cur_coins = int(f.read())
                    f.close()
                    f = open(coins_file, "wb")
                    f.write(str(cur_coins+num))
                    f.close()
            except:
                f = open("error_log.txt", 'a')
                f.write("Error parsing %s" % loot_string)
                f.close()

    return total_value    

f = open(total_loot_dir, "rb")
running_total = int(f.read().replace("\r", "").replace("\n", "").replace(",", ""))
f.close()
f = open(alltime_loot_dir, "rb")
alltime_total = int(f.read().replace("\r", "").replace("\n", "").replace(",", ""))
f.close()
f = open(webpage_dir, "wb")
f.write(webpage % (alltime_total+running_total, str("{0:.2f}".format((alltime_total+running_total)/float(1000000))), running_total, str("{0:.3f}".format(running_total/float(1000000)))))
f.close()	
	
while(True):

    try:
        f = open(manual_adjustment, "rb")
        manual_adjustment_amount = int(f.read().replace("\r", "").replace("\n", "").replace(",", ""))
        f.close()
        if manual_adjustment_amount != 0:
            print "Manually adjusting by: " + str(manual_adjustment_amount)
            f = open(total_loot_dir, "rb")
            running_total = int(f.read().replace("\r", "").replace("\n", "").replace(",", ""))
            f.close()
            print "Old running total: " + str(running_total)
            running_total+=manual_adjustment_amount
            f=open(total_loot_dir, "wb")
            f.write(str("{:,}".format(running_total)))
            f.close()
            f = open(manual_adjustment, "wb")
            f.write("0")
            f.close()
            f = open(webpage_dir, "wb")
            f.write(webpage % (alltime_total+running_total, str("{0:.2f}".format((alltime_total+running_total)/float(1000000))), running_total, str("{0:.3f}".format(running_total/float(1000000)))))
            f.close()
            print "New running total: " + str(running_total)
    except:
        print "Failed to apply manual adjustment. Check formatting in file."
			
    files = os.listdir(screenshot_dir)
    for a_file in files:
        if "Screenshot" in a_file:
            print "Checking " + str(a_file)
            string_list = get_valuable_drop_strings(screenshot_dir+"\\"+a_file)
            for astring in string_list:
                print astring
            total_value = parse_val_strings(string_list)
            print "Total value from that screenshot: " + str(total_value)
            f = open(total_loot_dir, "rb")
            running_total = int(f.read().replace("\r", "").replace("\n", "").replace(",", ""))
            f.close()
            running_total+=total_value

            f = open(hundredpercent_loot, 'rb')
            hundredpercent_loot_value = int(f.read().strip("\r").strip("\n"))
            f.close()
            print "100% loot: " + str(hundredpercent_loot_value)

            running_total+=hundredpercent_loot_value
            print "New total value: " + str("{:,}".format(running_total))
            f=open(total_loot_dir, "wb")
            f.write(str("{:,}".format(running_total)))
            f.close()
            new_ss_name = used_screenshot_dir+"\\Screenshot"+str(running_total)+"_"+str(uuid.uuid4()) + ".png"
            f = open(new_ss_name, 'a')
            f.close()
            f = open(alltime_loot_dir, "rb")
            alltime_total = int(f.read().replace("\r", "").replace("\n", "").replace(",", ""))
            f.close()
            f = open(webpage_dir, "wb")
            f.write(webpage % (alltime_total+running_total, str("{0:.2f}".format((alltime_total+running_total)/float(1000000))), running_total, str("{0:.3f}".format(running_total/float(1000000)))))
            f.close()
            shutil.copy2(screenshot_dir+"\\"+a_file, new_ss_name)
            os.remove(screenshot_dir+"\\"+a_file)
    time.sleep(10)

string_list = get_valuable_drop_strings("test.png")
print string_list

parse_val_strings(string_list)
print total_value
'''                
                    if len(adj_pixels) > 5:
                        try:
                            ld[str(apn)]
                        except KeyError:
                            print "(%d, %d)" % (x, y)
                            ld[str(apn)] = raw_input("Character ?")
    f = open("chardict.py", "wb")
    f.write("CHARACTER_DICT = " + str(ld))
    f.close()

'''
