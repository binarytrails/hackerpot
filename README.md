# IoT HackerPot

It allows its users to sense an invisible world of internet communications accordingly to which the HackerPot reacts. Its physical reaction informs the user of a possible malveillant intruder to make the person aware of this invisible presence. From this point, it is up to the user to define a way of dealing with this issue according to the type of alert received. This is a very promising first step into the direction of protecting the user's privacy by explicitly underlining the virtual abuse of rights happening in the network.

This IoT device is controlled by the means of a ```HackerPot.py``` class that can be used externally by any HoneyPot software. At the moment, I modified HoneyPy and its plugin TelnetDebian7 to recieve and call an instance of a HackerPot on the relevant moments to define attacks of interest.

*Made for Concordia University in the [CART 360](https://sevaivanov.github.io/cart360) class.*

![image](images/4.jpg)

## HackerPot + HoneyPy

	sudo python Honey.py -d
	
## Animations

	python HackerPotAnimationsTests.py

## Authors

Vsevolod (Seva) Ivanov - seva@tumahn.net
