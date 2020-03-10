from nonstory import Core

def test_random():
    players = ["A","B","C"]
    core = Core(players)
    assert len(core)==len(players)
    found_list = list()
    times = 0
    for x in core.random():
        if x == "":
            break
        else:
            ++times
            if x in found_list:
                #Does not return unique player list
                assert False
            elif x in players:
                found_list.append(x)
   
    assert (times == len(core) and
            len(core) == len(found_list))               
            
    