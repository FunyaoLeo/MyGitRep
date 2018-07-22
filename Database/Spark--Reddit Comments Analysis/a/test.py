#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Clean comment text for easier parsing."""

from __future__ import print_function

import re
import string
import argparse
import sys
import json
import operator

__author__ = "Fangyao Liu"
__email__ = "fangyaoliu@g.ucla.edu"


if __name__ == "__main__":
    # This is the Python main function.
    # You should be able to run
    # python cleantext.py <filename>
    # and this "main" function will open the file,
    # read it line by line, extract the proper value from the JSON,
    # pass to "sanitize" and print the result as a list.

    # YOUR CODE GOES BELOW.
    para=sys.argv
    
    cnt=0
    i=0
    with open('sample-output.txt','r') as s:
        with open('output.txt','r') as f:
            try:
                while i<1000:
                    i+=1
                    answer=s.readline()
                    result=f.readline()
                  
                    if answer:
                        if (operator.eq(answer,result)==True):
                            cnt+=1
                            #print(success)
                        else:
                            print(i-1)
                            print(result)
                            print(answer)
                    else: 
                        break
            except:
                f.close()
    print (cnt/100)
    #text = "this is a test https://sdfs.sdfsdf.com/sdfsdf/sdfsdf/sd/sdfsdfs?bob=%20tree&jef=man lets see this too https://sdfsdf.fdf.com/sdf/f end"
    #sanitize(text)
