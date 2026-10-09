import csv
from collections import defaultdict
from collections.abc import Iterator
from itertools import groupby


def bball(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        # URL,GameType,Location,Date,Time,WinningTeam,Quarter,SecLeft,AwayTeam,AwayPlay,AwayScore,HomeTeam,HomePlay,HomeScore,Shooter,ShotType,ShotOutcome,ShotDist,Assister,Blocker,FoulType,Fouler,Fouled,Rebounder,ReboundType,ViolationPlayer,ViolationType,TimeoutTeam,FreeThrowShooter,FreeThrowOutcome,FreeThrowNum,EnterGame,LeaveGame,TurnoverPlayer,TurnoverType,TurnoverCause,TurnoverCauser,JumpballAwayPlayer,JumpballHomePlayer,JumpballPoss,
        ball_reader = csv.DictReader(f)
        for line in ball_reader:
            URL = line["URL"]
            Quarter = int(line["Quarter"])
            SecLeft = int(line["SecLeft"])
            game_id = URL.removeprefix("/boxscores/").removesuffix(".html")
            time = 12 * 60 * Quarter - SecLeft
            if Quarter >= 5:
                OTs = Quarter - 4
                time = 12 * 60 * 4 + 300*OTs - SecLeft
            home_diff = int(line["HomeScore"]) - int(line["AwayScore"])
            if line["WinningTeam"] == line["HomeTeam"]:
                winner_diff = home_diff
            else:
                winner_diff = -home_diff
            yield game_id, time, winner_diff


def respan(group: Iterator[tuple[str, int, int]], interval):
    """
    Takes an iterator of tuples of id, time, score
    and yields tuples of time, score where time is a multiple of 30
    :param group:
    :return:
    """
    prev_time = 0
    prev_score = 0
    for _, time, winner_diff in group:
        while prev_time < time:
            yield prev_time, prev_score
            prev_time += interval
        prev_score = winner_diff
    yield time, winner_diff

def main(test_file, interval=60):
    # {time : {split: [wins, losses]}}
    matrix = defaultdict(lambda: defaultdict(lambda: [0,0]))
    for game_id, group in groupby(bball(test_file), lambda x: x[0]):
        for time, winner_diff in respan(group, interval):
            matrix[time][winner_diff][0] += 1
            matrix[time][-winner_diff][1] += 1

    min_split = min(min(split_map.keys()) for split_map in matrix.values())
    max_time = max(matrix.keys())

    print("\t", end="")
    print(*range(0, max_time, interval), sep="\t")
    for split in reversed(range(min_split, -min_split + 1)):
        line = []
        # i need to graph the points (time, spread, wins/(wins+losses))
        for time in range(0, max_time, interval):
            wins, losses = matrix[time][split]
            if wins + losses == 0:
                line.append("")
            else:
                line.append(f"={wins}/{wins + losses}")
        print(split, *line, sep="\t")
        pass


if __name__ == '__main__':
    main("basketball_data/2019-20_pbp.csv")
