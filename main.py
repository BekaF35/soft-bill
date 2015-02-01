#!/usr/bin/env python
"""
Soft Bill is a virtual, RS-232 bill validator
@auth@or: me@corytodd.us
@version: 0.2

TODO: Implement master timeout (no poll, we must disable ourselves)
TODO: More useful cheat mocking
TODO: Check ACK number, resend last message if required
"""
import acceptor
import sys


### Main  Routine ###
def main(portname):
    """
    Application to simulate hardware bill validator

    Args:
        portname -- string portname e.g. COM2, /dev/tty.*
    """

    slave = acceptor.Acceptor()

    cmd_table = '''

    H or ? to show Help
    Q or CTRL+C to Quit

    Bill position to simulate bill insertions:
    1 - $1   or 1st note
    2 - $2   or 2nd note
    3 - $5   or 3rd note
    4 - $10  or 4th note
    5 - $20  or 5th note
    6 - $50  or 6th note
    7 - $100 or 7th note

    Note:
    Software automatically changes states once mock bill insertion begins
    Idling->Accepting->Escrowed->{Stacking,Returning}->{Stacked,Returned}

    Toggle Events:
    C - Cheated
    R - Rejected (We think note is invalid)
    J - Jammed
    F - Stacker Full
    P - LRC present (cashbox: set to 1 means it's there)

    Extra Stuff:
    W - Powering up
    I - Invalid Command was received
    X - Failure (This BA has failed)
    Y - Empty Cashbox
    
    Bill Disable and Enables:
    Dx - where x is the index to disable (e.g. D1 disables $1)
    Ex - where x in the index to enable  (e.g. E1 enables $1)
    
    '''


    print "Starting software BA on port {:s}".format(portname)
    slave.start(portname)

    # Loop until we are to exit
    try:
        print cmd_table
        while slave.running:

            cmd = raw_input()
            result = slave.parse_cmd(cmd)
            if result is 0:
                pass
            elif result is 1:
                slave.stop()
            elif result is 2:
                print cmd_table

    except KeyboardInterrupt:
        slave.running = False

    print '\n\nGoodbye!'
    print 'Port {:s} closed'.format(portname)

if __name__ == "__main__":
    main(sys.argv[1])
