# gwificcbcast
Google Wifi and Ethernet WAN Chromecast - broadcast forwarder

The purpose of this project is to help whoever have an ethernet chromecast (like Nvidia Shield) connected to their main router,
and have problems using it with attached Google Wifi (which forces NAT to user Mesh)

What is done here is helping the ethernet chromecast to broadcast itself inside the NAT

We are listening to the broadcast messag (mDns, port 5353) and forwarding it to a server inside the Google wifi nat, and then rebroadcast it

What is needed:

1. A device connected to the outer NAT network
2. A device connected to the google wifi network
3. Port forward port 5353 to the device inside the google wifi network
4. Recommended - assign the google wifi and chromecast with static addresses
5. Python3 installed on both devices
6. Run the server inside the Google Wifi network
7. Run the mcast script in the outer network

That's it
Feel free to use, alter and improve

What can I say - It works for me

