import redis

match_length = 60*7 
STATE_ENTER = 0x01
STATE_BOOT  = 0x02
STATE_LIVE  = 0x04
STATE_SCORE = 0x08


r = redis.Redis(host='localhost', port=6379, db=0)

def get_next_match():
    global r;
    len = r.llen("org.srobo.matches") 
    comptime = float(r.get("org.srobo.time.competition"))
    for i in xrange(0, len):
        v = r.lindex("org.srobo.matches", i)
        match = match_from_ms(v)
        if match["time"] > comptime and match["time"] < comptime + match_length:
            return match

    return match_from_ms(r.lindex("org.srobo.matches", index))

def get_current_match():
    global r;
    len = r.llen("org.srobo.matches") 
    comptime = float(r.get("org.srobo.time.competition"))
    for i in xrange(0, len):
        v = r.lindex("org.srobo.matches", i)
        match = match_from_ms(v)
        upper = match["time"] + match_length
        lower = match["time"]
        if comptime > lower and comptime < upper:
            return match

def get_current_state():
    global r
    current_match = get_current_match()
    comptime = float(r.get("org.srobo.time.competition"))
    into_match = comptime-current_match["time"]
    minute = into_match/60
    print minute
    if minute <= 1:
        return STATE_ENTER
    elif minute > 1 and minute <= 2:
        return STATE_BOOT
    elif minute > 2 and minute <= 5:
        return STATE_LIVE
    elif minute > 5 and minute <= 7:
        return STATE_SCORE

    
def match_from_ms(ms):
    match = ms.split(",")
    match_dict = {"time": float(match[0]),
                  "teams": [ int(x) for x in match[1:-1]]}
    match_dict["number"] = match[-1]
    return match_dict

if __name__ == "__main__":
    time = r.get("org.srobo.time.competition")
    print time
    print get_current_match()
    print get_next_match()
    print get_current_state()
