from solution1 import HandheldDevice

def test_1(): 
    hd = HandheldDevice(0, 0, 9, [2, 6])
    hd.run()
    assert 1 == hd.register_b

def test_2():
    hd = HandheldDevice(10, 0, 0, [5,0,5,1,5,4])
    hd.run()
    assert '0,1,2' == hd.output 

def test_3():
    hd = HandheldDevice(2024, 0, 0, [0,1,5,4,3,0])
    hd.run()
    assert '4,2,5,6,7,7,7,7,3,1,0' == hd.output
    assert 0 == hd.register_a

def test_4():
    hd = HandheldDevice(0, 29, 0, [1,7])
    hd.run()
    assert 26 == hd.register_b

def test_5():
    hd = HandheldDevice(0, 2024, 43690, [4,0])
    hd.run()
    assert 44354 == hd.register_b

def test_blah():
    hd = HandheldDevice(64, 0, 0, [0, 3])
    hd.run()
    assert 8 == hd.register_a
