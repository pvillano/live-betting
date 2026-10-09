import csv


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
    test_file = "basketball_data/2019-20_pbp.csv"
    prev_split = 999
    prev_id = "asdfawef"
    rows = 0
    out_rows = 0
    with open("out.csv", "w") as f:
        f.write("id,time,winner_diff\n")
        for line in bball(test_file):
            game_id, time, winner_diff = line
            rows += 1
            if winner_diff == prev_split and game_id == prev_id:
                continue
            prev_id = game_id
            prev_split = winner_diff
            f.write(",".join(map(str, line)) + "\n")
            out_rows += 1
    print(f"Wrote {out_rows} out of {rows} rows to out.csv")


if __name__ == '__main__':
    main()
