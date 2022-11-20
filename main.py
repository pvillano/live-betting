import csv


def bball(file_name):
    with open(file_name, "r") as f:
        # URL,GameType,Location,Date,Time,WinningTeam,Quarter,SecLeft,AwayTeam,AwayPlay,AwayScore,HomeTeam,HomePlay,HomeScore,Shooter,ShotType,ShotOutcome,ShotDist,Assister,Blocker,FoulType,Fouler,Fouled,Rebounder,ReboundType,ViolationPlayer,ViolationType,TimeoutTeam,FreeThrowShooter,FreeThrowOutcome,FreeThrowNum,EnterGame,LeaveGame,TurnoverPlayer,TurnoverType,TurnoverCause,TurnoverCauser,JumpballAwayPlayer,JumpballHomePlayer,JumpballPoss,
        ball_reader = csv.DictReader(f)
        for line in ball_reader:
            id = f'{line["Date"]} {line["HomeTeam"]} vs {line["AwayTeam"]}'
            time = 12 * 60 * (int(line["Quarter"]) - 1) + (12 * 60 - int(line["SecLeft"]))
            home_diff = int(line["HomeScore"]) - int(line["AwayScore"])
            if line["WinningTeam"] == line["HomeTeam"]:
                winner_diff = home_diff
            else:
                winner_diff = -home_diff
            yield id, time, winner_diff


def main():
    test_file = "basketball_data/2019-20_pbp.csv"
    id = next(bball(test_file))[0]
    for line in bball(test_file):
        if line[0] != id:
            break
        print(line)


if __name__ == '__main__':
    main()
