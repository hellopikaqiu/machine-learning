import os

#this header needed for read_csv funciton in pandas library
header="duration,protocol_type,service,flag,src_bytes,dst_bytes,land,wrong_fragment,urgent,count,srv_count,serror_rate,srv_serror_rate,rerror_rate,srv_rerror_rate,same_srv_rate,diff_srv_rate,srv_diff_host_rate,dst_host_count,dst_host_srv_count,dst_host_same_srv_rate,dst_host_diff_srv_rate,dst_host_same_src_port_rate,dst_host_srv_diff_host_rate,dst_host_serror_rate,dst_host_srv_serror_rate,dst_host_rerror_rate,dst_host_srv_rerror_rate,label"

#http://kdd.ics.uci.edu/databases/kddcup99/training_attack_types
deleted_labels = ["buffer_overflow",
"ftp_write",
"guess_passwd",
"imap",
"ipsweep",
"loadmodule",
"multihop",
"nmap",
"perl",
"phf",
"portsweep",
"rootkit",
"satan",
"spy",
"warezclient",
"warezmaster"]

aggregated_labels = {"back":"dos",
"land":"dos",
"neptune":"dos",
"pod":"dos",
"smurf":"dos",
"teardrop":"dos",
"normal":"normal"}

#cat kddcup.data_10_percent_corrected | cut -d"," -f2 | sort | uniq
protocol_types = {"icmp":0,
"tcp":1,
"udp":2}

#cat kddcup.data_10_percent_corrected | cut -d"," -f3 | sort | uniq
services = {"auth":0,
"bgp":1,
"courier":2,
"csnet_ns":3,
"ctf":4,
"daytime":5,
"discard":6,
"domain":7,
"domain_u":8,
"echo":9,
"eco_i":10,
"ecr_i":11,
"efs":12,
"exec":13,
"finger":14,
"ftp":15,
"ftp_data":16,
"gopher":17,
"hostnames":18,
"http":19,
"http_443":20,
"imap4":21,
"IRC":22,
"iso_tsap":23,
"klogin":24,
"kshell":25,
"ldap":26,
"link":27,
"login":28,
"mtp":29,
"name":30,
"netbios_dgm":31,
"netbios_ns":32,
"netbios_ssn":33,
"netstat":34,
"nnsp":35,
"nntp":36,
"ntp_u":37,
"other":38,
"pm_dump":39,
"pop_2":40,
"pop_3":41,
"printer":42,
"private":43,
"red_i":44,
"remote_job":45,
"rje":46,
"shell":47,
"smtp":48,
"sql_net":49,
"ssh":50,
"sunrpc":51,
"supdup":52,
"systat":53,
"telnet":54,
"tftp_u":55,
"time":56,
"tim_i":57,
"urh_i":58,
"urp_i":59,
"uucp":60,
"uucp_path":61,
"vmnet":62,
"whois":63,
"X11":64,
"Z39_50":65}

#cat kddcup.data_10_percent_corrected | cut -d"," -f4 | sort | uniq
flags = {"OTH":0,
"REJ":1,
"RSTO":2,
"RSTOS0":3,
"RSTR":4,
"S0":5,
"S1":6,
"S2":7,
"S3":8,
"SF":9,
"SH":10}

#deleting host based features
#label deleted also for further aggregating
deleted_features = [42]
for i in range(10,23):
	deleted_features.append(i)
deleted_features.sort()
deleted_features.reverse()


filename = "kddcup_data"
uniq_filename = "uniq_" + filename
os.system("cat " + filename + " | sort | uniq > " + uniq_filename)


file = open(uniq_filename,"r")

new_filename = "preprocessed_" + filename
new_file = open(new_filename,"w")
new_file.write(header+"\n")

for line in file:
	line = line.replace("\n","")
	tokens = line.split(",")

	label = tokens[41]
	label = label.replace(".","")

	if label not in deleted_labels:
		label = aggregated_labels[label]

		tokens[1] = str(protocol_types[tokens[1]])
		tokens[2] = str(services[tokens[2]])
		tokens[3] = str(flags[tokens[3]])

		for i in deleted_features:
			tokens.pop(i-1)

		tokens.append(label)
		#print ",".join(tokens)
		new_file.write(",".join(tokens) + "\n")


file.close()
new_file.close()

print "File created: " + "uniq_" + filename
print "File created: " + new_filename

print "\nSize Information"
os.system("wc -l " + filename)
os.system("wc -l " + uniq_filename)
os.system("wc -l " + new_filename)