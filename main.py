import csv
from itertools import groupby


def bball(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        # URL,GameType,Location,Date,Time,WinningTeam,Quarter,SecLeft,AwayTeam,AwayPlay,AwayScore,HomeTeam,HomePlay,HomeScore,Shooter,ShotType,ShotOutcome,ShotDist,Assister,Blocker,FoulType,Fouler,Fouled,Rebounder,ReboundType,ViolationPlayer,ViolationType,TimeoutTeam,FreeThrowShooter,FreeThrowOutcome,FreeThrowNum,EnterGame,LeaveGame,TurnoverPlayer,TurnoverType,TurnoverCause,TurnoverCauser,JumpballAwayPlayer,JumpballHomePlayer,JumpballPoss,
        ball_reader = csv.DictReader(f)
        for line in ball_reader:
            id = line["URL"].removeprefix("/boxscores/").removesuffix(".html")
            time = 12 * 60 * (int(line["Quarter"]) - 1) + (12 * 60 - int(line["SecLeft"]))
            home_diff = int(line["HomeScore"]) - int(line["AwayScore"])
            if line["WinningTeam"] == line["HomeTeam"]:
                winner_diff = home_diff
            else:
                winner_diff = -home_diff
            yield id, time, winner_diff


def main():
    rows = 0
    out_rows = 0
    test_file = "basketball_data/2019-20_pbp.csv"
    for k, group in groupby(bball(test_file), lambda x: x[0]):
        with open(f"out/{k}.csv", "w+", encoding="utf-8") as f:
            f.write("time,winner_diff\n")
            prev_diff = 999
            for game_id, time, winner_diff in group:
                rows += 1
                if prev_diff != winner_diff:
                    f.write(f"{time}, {winner_diff}\n")
                    out_rows += 1
                prev_diff = winner_diff
    print(f"Wrote {out_rows} out of {rows} rows")


if __name__ == '__main__':
    main()
