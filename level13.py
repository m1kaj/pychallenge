"""http://www.pythonchallenge.com/pc/return/disproportional.html
"""

# login credentials when returning are still: huge/file
#
# Page has an image of a phone keypad. Number '5' button
# is clickable. Link leads to http://www.pythonchallenge.com/pc/phonebook.php
#
# Linked page returns an XML document that starts with:
#
#<methodResponse>
#  <fault>
#    <value>
#      <struct>
#        <member>
#          <name>faultCode</name>
#        <value>
#          <int>105</int>
#
# Putting those tags to Google search returns hits talking about something
# called XMLRPC. Remote Procedure Calls protocol using XML? Seems so. It works
# over HTTP. Developed by Dave Winer in 1998. 
# Basics and history: https://en.wikipedia.org/wiki/XML-RPC
#
# Python has a client and server library for XMLRPC. No surprise there :)
# https://docs.python.org/3/library/xmlrpc.client.html#module-xmlrpc.client
#
# Lets's just play a bit using the above docs:

from xmlrpc.client import ServerProxy, Error

with ServerProxy("http://www.pythonchallenge.com/pc/phonebook.php") as proxy:
    try:
        for method in proxy.system.listMethods():
            print(f"Signature and help for method: {method}:")
            print(f"    {proxy.system.methodSignature(method)}")
            print(f"    {proxy.system.methodHelp(method)}")
    except Error as ev:
        print(f"Error happened: {ev}")

# Signature and help for method: phone:
#     [['string', 'string']]
#     Returns the phone of a person
# Signature and help for method: system.listMethods:
#     [['array']]
#     This method lists all the methods that the XML-RPC server knows how to dispatch
# Signature and help for method: system.methodHelp:
#     [['string', 'string']]
#     Returns help text if defined for the method passed, otherwise returns an empty string
# Signature and help for method: system.methodSignature:
#     [['array', 'string']]
#     Returns an array of known signatures (an array of arrays) for the method name passed. If no signatures are known, returns a none-array (test for type != array to detect missing signature)
# Signature and help for method: system.multicall:
#     [['array', 'array']]
#     Boxcar multiple RPC calls in one request. See http://www.xmlrpc.com/discuss/msgReader$1208 for details
# Signature and help for method: system.getCapabilities:
#     [['struct']]
#     This method lists all the capabilites that the XML-RPC server has: the (more or less standard) extensions to the xmlrpc spec that it adheres to
#
# The only non-standard method seems to be "phone". We'll just ask a numbers for some
# imaginary persons then:

    try:
        num1 = proxy.phone("Barry Boring")
        num2 = proxy.phone("Yannis Yawn")
    except Error as ev:
        print(f"Error happened: {ev}")
    print(f"Barry:  {num1}")
    print(f"Yannis: {num2}")

# Barry:  He is not the evil
# Yannis: He is not the evil
#
# Ok. Who is the person then? The initial image of the phone keypad had text under it: "phone that evil"
# It's frustrating to try to guess then name based on the string "evil". All these just return the same hint:

    evils = ["Evil", "evil2", "evil2.gfx", "Live", "live", "devil", "Devil", "Satan"]
    for name in evils:
        number = proxy.phone(name)
        print(f"{name} : {number}")

# I had to Google this. In the previous challenge there were jpg files. The last file did not display in Firefox,
# browser said the image has errors and cannot be displayed: http://www.pythonchallenge.com/pc/return/evil4.jpg
# Going back to it, the file is too small for JPG. File contents are just: "Bert is evil! Go back!"
#
# I tried Edge browser and it displays text without issues. Firefox on the other hand seems to refuse to display
# anything except and error notice when it cannot decode the file as an image. Both approaches have their
# pros and cons, I think.

    print(f"Bert: {proxy.phone('Bert')}")
#
# returns: 555-ITALY
#
# answer turns out to be "italy"