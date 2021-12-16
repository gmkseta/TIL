while [ "$input" != "exit" ]; do
  echo "문제 번호 입력: "
  read input
  if [ "$input" = "exit" ]; then
    echo "exit"
    if [ -z ${row+x} ]; then
      echo "바로 나가버리기"
    else
      th="| 문제 | 링크 | Lv  | Solved? | \n| ------------------------- | -------------------------------------------------------- | --- | ------- |"
      awk -v row="$th" 'NR==5{print row}1' readme.md >readme.md.tmp
      echo "$(cat readme.md.tmp)" >readme.md
    fi
    rm readme.md.tmp

  elif ! [[ $input =~ ^[0-9]+$ ]]; then
    echo "숫자를 입력해주세요"
    continue
  else
    boj_link="https://www.acmicpc.net/problem/$input"
    echo "문제 링크: $boj_link"
    title=$(curl -s -N "$boj_link" | sed -n "s/^.*<title>\(.*\)<\/title>.*$/\1/p")
    title=${title#*: }
    sovled_link="https://solved.ac/search?query=$input"

    # get tier from solved link parsing from html , img tag who has class like 'TierBadge__Tier'
    tier=$(curl -s -N https://solved.ac/search\?query\=$input | sed -n 's/.*alt="\(.*\)" class="TierBadge__Tier.*>/\1/p')

    echo $tier

    row="| $title | $boj_link | $tier | |"

    awk -v row="$row" 'NR==5{print row}1' readme.md >readme.md.tmp
    echo "$(cat readme.md.tmp)" >readme.md

  fi

done
