from subprocess import Popen, PIPE
import os
f = 'test.py'

tests = [('2 2', '4'),
         ('2 2', '123')]


test_count = 1
for test_in, test_out in tests:
    p = Popen(['python ' + os.getcwd() + '/' + 'test.py'], stdout=PIPE, stdin=PIPE, shell=True)
    stdout = p.communicate(input=test_in)[0]
    out = stdout.decode().strip()
    if test_out == out:
        print '.',
    else:
        print '\n---------------'
        print 'Test #' + str(test_count)
        print
        print 'Expected:'
        print test_out
        print 'Out:'
        print out
        print '---------------'
    test_count += 1
print
