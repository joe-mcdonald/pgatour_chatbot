import requests
import pandas as pd

# Endpoint and headers
url = "https://orchestrator.pgatour.com/graphql"
headers = {
    "x-api-key": "da2-gsrx5bibzbb4njvhl7t37wqyl4",
    "content-type": "application/json",
    "origin": "https://www.pgatour.com",
    "referer": "https://www.pgatour.com"
}

links = {
    "https://www.pgatour.com/player/49303/anders-albertson",
    "https://www.pgatour.com/player/33948/byeong-hun-an",
    "https://www.pgatour.com/player/52370/mason-andersen",
    "https://www.pgatour.com/player/52955/ludvig-aberg",
    "https://www.pgatour.com/player/22371/aaron-baddeley",
    "https://www.pgatour.com/player/40026/daniel-berger",
    "https://www.pgatour.com/player/45522/christiaan-bezuidenhout",
    "https://www.pgatour.com/player/56630/akshay-bhatia",
    "https://www.pgatour.com/player/40058/zac-blair",
    "https://www.pgatour.com/player/33141/keegan-bradley",
    "https://www.pgatour.com/player/34255/joseph-bramlett",
    "https://www.pgatour.com/player/28420/ryan-brehm",
    "https://www.pgatour.com/player/60004/jacob-bridgeman",
    "https://www.pgatour.com/player/48084/wesley-bryan",
    "https://www.pgatour.com/player/55708/hayden-buckley",
    "https://www.pgatour.com/player/29268/bronson-burgoon",
    "https://www.pgatour.com/player/47504/sam-burns",
    "https://www.pgatour.com/player/46443/brian-campbell",
    "https://www.pgatour.com/player/32070/rafael-campos",
    "https://www.pgatour.com/player/32070/rafael-campos",
    "https://www.pgatour.com/player/35450/patrick-cantlay",
    "https://www.pgatour.com/player/49590/frankie-capan-iii",
    "https://www.pgatour.com/player/59440/ricky-castillo",
    "https://www.pgatour.com/player/34021/bud-cauley",
    "https://www.pgatour.com/player/52372/cameron-champ",
    "https://www.pgatour.com/player/58933/will-chandler",
    "https://www.pgatour.com/player/32366/kevin-chappell",
    "https://www.pgatour.com/player/20229/stewart-cink",
    "https://www.pgatour.com/player/66743/luke-clanton",
    "https://www.pgatour.com/player/51766/wyndham-clark",
    "https://www.pgatour.com/player/47591/eric-cole",
    "https://www.pgatour.com/player/49453/trevor-cone",
    "https://www.pgatour.com/player/39997/corey-conners",
    "https://www.pgatour.com/player/59442/parker-coody",
    "https://www.pgatour.com/player/59836/pierceson-coody",
    "https://www.pgatour.com/player/46435/austin-cook",
    "https://www.pgatour.com/player/32982/vince-covello",
    "https://www.pgatour.com/player/52514/trace-crowe",
    "https://www.pgatour.com/player/58605/quade-cummins",
    "https://www.pgatour.com/player/39067/mj-daffue",
    "https://www.pgatour.com/player/34076/joel-dahmen",
    "https://www.pgatour.com/player/45157/cam-davis",
    "https://www.pgatour.com/player/28089/jason-day",
    "https://www.pgatour.com/player/39859/cristobal-del-solar",
    "https://www.pgatour.com/player/33653/thomas-detry",
    "https://www.pgatour.com/player/51690/taylor-dickson",
    "https://www.pgatour.com/player/50497/adrien-dumont-de-chassart",
    "https://www.pgatour.com/player/45609/tyler-duncan",
    "https://www.pgatour.com/player/59866/nick-dunlap",
    "https://www.pgatour.com/player/51349/nico-echavarria",
    "https://www.pgatour.com/player/57362/austin-eckroat",
    "https://www.pgatour.com/player/47079/harrison-endycott",
    "https://www.pgatour.com/player/34099/harris-english",
    "https://www.pgatour.com/player/29725/tony-finau",
    "https://www.pgatour.com/player/54576/patrick-fishburn",
    "https://www.pgatour.com/player/57123/steven-fisk",
    "https://www.pgatour.com/player/40098/matt-fitzpatrick",
    "https://www.pgatour.com/player/30911/tommy-fleetwood",
    "https://www.pgatour.com/player/65256/david-ford",
    "https://www.pgatour.com/player/32102/rickie-fowler",
    "https://www.pgatour.com/player/29936/ryan-fox",
    "https://www.pgatour.com/player/29535/brice-garnett",
    "https://www.pgatour.com/player/19846/brian-gay",
    "https://www.pgatour.com/player/59018/ryan-gerard",
    "https://www.pgatour.com/player/52375/doug-ghim",
    "https://www.pgatour.com/player/25900/lucas-glover",
    "https://www.pgatour.com/player/28679/fabian-gomez",
    "https://www.pgatour.com/player/55165/noah-goodwin",
    "https://www.pgatour.com/player/56762/will-gordon",
    "https://www.pgatour.com/player/59095/chris-gotterup",
    "https://www.pgatour.com/player/51977/max-greyserman",
    "https://www.pgatour.com/player/54591/ben-griffin",
    "https://www.pgatour.com/player/35310/lanto-griffin",
    "https://www.pgatour.com/player/31646/emiliano-grillo",
    "https://www.pgatour.com/player/24924/bill-haas",
    "https://www.pgatour.com/player/34563/chesson-hadley",
    "https://www.pgatour.com/player/33399/adam-hadwin",
    "https://www.pgatour.com/player/32448/james-hahn",
    "https://www.pgatour.com/player/57975/harry-hall",
    "https://www.pgatour.com/player/47988/nick-hardy",
    "https://www.pgatour.com/player/27644/brian-harman",
    "https://www.pgatour.com/player/34098/russell-henley",
    "https://www.pgatour.com/player/49298/kramer-hickok",
    "https://www.pgatour.com/player/54421/garrick-higgo",
    "https://www.pgatour.com/player/33597/harry-higgs",
    "https://www.pgatour.com/player/60067/joe-highsmith",
    "https://www.pgatour.com/player/51287/ryo-hisatsune",
    "https://www.pgatour.com/player/54628/lee-hodges",
    "https://www.pgatour.com/player/51696/rico-hoey",
    "https://www.pgatour.com/player/12716/charley-hoffman",
    "https://www.pgatour.com/player/35532/tom-hoge",
    "https://www.pgatour.com/player/52453/nicolai-hjgaard",
    "https://www.pgatour.com/player/52686/rasmus-hjgaard",
    "https://www.pgatour.com/player/27141/j.b-holmes",
    "https://www.pgatour.com/player/39977/max-homa",
    "https://www.pgatour.com/player/29420/billy-horschel",
    "https://www.pgatour.com/player/47056/rikuya-hoshino",
    "https://www.pgatour.com/player/35461/beau-hossler",
    "https://www.pgatour.com/player/46717/viktor-hovland",
    "https://www.pgatour.com/player/36801/mark-hubbard",
    "https://www.pgatour.com/player/35506/mackenzie-hughes",
    "https://www.pgatour.com/player/34174/john-huh",
    "https://www.pgatour.com/player/39971/sungjae-im",
    "https://www.pgatour.com/player/36799/stephan-jaeger",
    "https://www.pgatour.com/player/24024/zach-johnson",
    "https://www.pgatour.com/player/47917/takumi-kanaya",
    "https://www.pgatour.com/player/34587/chan-kim",
    "https://www.pgatour.com/player/39975/michael-kim",
    "https://www.pgatour.com/player/50188/s.h-kim",
    "https://www.pgatour.com/player/37455/si-woo-kim",
    "https://www.pgatour.com/player/55182/tom-kim",
    "https://www.pgatour.com/player/30926/chris-kirk",
    "https://www.pgatour.com/player/29478/kevin-kisner",
    "https://www.pgatour.com/player/48117/kurt-kitayama",
    "https://www.pgatour.com/player/32757/patton-kizzire",
    "https://www.pgatour.com/player/47420/jake-knapp",
    "https://www.pgatour.com/player/54813/philip-knowles",
    "https://www.pgatour.com/player/33122/russell-knox",
    "https://www.pgatour.com/player/36884/ben-kohles",
    "https://www.pgatour.com/player/23108/matt-kuchar",
    "https://www.pgatour.com/player/27936/martin-laird",
    "https://www.pgatour.com/player/28775/nate-lashley",
    "https://www.pgatour.com/player/45523/thriston-lawrence",
    "https://www.pgatour.com/player/32791/k.h-lee",
    "https://www.pgatour.com/player/37378/min-woo-lee",
    "https://www.pgatour.com/player/37278/nicholas-lindheim",
    "https://www.pgatour.com/player/34409/david-lingmerth",
    "https://www.pgatour.com/player/36326/david-lipsky",
    "https://www.pgatour.com/player/27129/luke-list",
    "https://www.pgatour.com/player/35449/adam-long",
    "https://www.pgatour.com/player/40162/justin-lower",
    "https://www.pgatour.com/player/33204/shane-lowry",
    "https://www.pgatour.com/player/52215/robert-macintyre",
    "https://www.pgatour.com/player/34466/peter-malnati",
    "https://www.pgatour.com/player/33199/matteo-manassero",
    "https://www.pgatour.com/player/33413/ben-martin",
    "https://www.pgatour.com/player/32839/hideki-matsuyama",
    "https://www.pgatour.com/player/51491/brandon-matthews",
    "https://www.pgatour.com/player/51491/brandon-matthews",
    "https://www.pgatour.com/player/51491/brandon-matthews",
    "https://www.pgatour.com/player/47993/denny-mccarthy",
    "https://www.pgatour.com/player/59141/matt-mccarty",
    "https://www.pgatour.com/player/40042/tyler-mccumber",
    "https://www.pgatour.com/player/51950/max-mcgreevy",
    "https://www.pgatour.com/player/28237/rory-mcilroy",
    "https://www.pgatour.com/player/46442/maverick-mcnealy",
    "https://www.pgatour.com/player/59143/mac-meissner",
    "https://www.pgatour.com/player/32640/troy-merritt",
    "https://www.pgatour.com/player/39546/keith-mitchell",
    "https://www.pgatour.com/player/25198/francesco-molinari",
    "https://www.pgatour.com/player/55789/taylor-montgomery",
    "https://www.pgatour.com/player/26596/ryan-moore",
    "https://www.pgatour.com/player/49947/taylor-moore",
    "https://www.pgatour.com/player/50525/collin-morikawa",
    "https://www.pgatour.com/player/63121/william-mouw",
    "https://www.pgatour.com/player/46601/trey-mullinax",
    "https://www.pgatour.com/player/36871/matt-nesmith",
    "https://www.pgatour.com/player/29289/s.y-noh",
    "https://www.pgatour.com/player/27349/alex-noren",
    "https://www.pgatour.com/player/35706/niklas-norgaard",
    "https://www.pgatour.com/player/30163/henrik-norlander",
    "https://www.pgatour.com/player/51070/vincent-norrman",
    "https://www.pgatour.com/player/51997/andrew-novak",
    "https://www.pgatour.com/player/24140/sean-ohair",
    "https://www.pgatour.com/player/33968/thorbjrn-olesen",
    "https://www.pgatour.com/player/55623/kaito-onishi",
    "https://www.pgatour.com/player/59160/john-pak",
    "https://www.pgatour.com/player/23320/ryan-palmer",
    "https://www.pgatour.com/player/20572/rod-pampling",
    "https://www.pgatour.com/player/29908/c.t-pan",
    "https://www.pgatour.com/player/50582/jeremy-paul",
    "https://www.pgatour.com/player/48153/matthieu-pavon",
    "https://www.pgatour.com/player/40250/taylor-pendrith",
    "https://www.pgatour.com/player/47679/victor-perez",
    "https://www.pgatour.com/player/36824/paul-peterson",
    "https://www.pgatour.com/player/57900/chandler-phillips",
    "https://www.pgatour.com/player/25818/scott-piercy",
    "https://www.pgatour.com/player/49771/j.t-poston",
    "https://www.pgatour.com/player/63343/aldrich-potgieter",
    "https://www.pgatour.com/player/28252/seamus-power",
    "https://www.pgatour.com/player/34256/andrew-putnam",
    "https://www.pgatour.com/player/46414/aaron-rai",
    "https://www.pgatour.com/player/47983/chad-ramey",
    "https://www.pgatour.com/player/26476/chez-reavie",
    "https://www.pgatour.com/player/64693/matthew-riedel",
    "https://www.pgatour.com/player/47995/davis-riley",
    "https://www.pgatour.com/player/36699/patrick-rodgers",
    "https://www.pgatour.com/player/22405/justin-rose",
    "https://www.pgatour.com/player/60882/thomas-rosenmueller",
    "https://www.pgatour.com/player/39335/kevin-roy",
    "https://www.pgatour.com/player/46646/antoine-rozner",
    "https://www.pgatour.com/player/37275/sam-ryder",
    "https://www.pgatour.com/player/56781/isaiah-salinda",
    "https://www.pgatour.com/player/64442/gordon-sargent",
    "https://www.pgatour.com/player/48081/xander-schauffele",
    "https://www.pgatour.com/player/46046/scottie-scheffler",
    "https://www.pgatour.com/player/47347/adam-schenk",
    "https://www.pgatour.com/player/48867/matti-schmid",
    "https://www.pgatour.com/player/24502/adam-scott",
    "https://www.pgatour.com/player/46441/robby-shelton",
    "https://www.pgatour.com/player/51890/greyson-sigg",
    "https://www.pgatour.com/player/39327/ben-silverman",
    "https://www.pgatour.com/player/29221/webb-simpson",
    "https://www.pgatour.com/player/06567/vijay-singh",
    "https://www.pgatour.com/player/27139/david-skinns",
    "https://www.pgatour.com/player/46340/alex-smalley",
    "https://www.pgatour.com/player/27649/brandt-snedeker",
    "https://www.pgatour.com/player/39324/j.j-spaun",
    "https://www.pgatour.com/player/34046/jordan-spieth",
    "https://www.pgatour.com/player/50484/hayden-springer",
    "https://www.pgatour.com/player/30692/scott-stallings",
    "https://www.pgatour.com/player/51600/jimmy-stanger",
    "https://www.pgatour.com/player/30110/kyle-stanley",
    "https://www.pgatour.com/player/55893/sam-stevens",
    "https://www.pgatour.com/player/49960/sepp-straka",
    "https://www.pgatour.com/player/27214/kevin-streelman",
    "https://www.pgatour.com/player/60019/jackson-suber",
    "https://www.pgatour.com/player/40115/adam-svensson",
    "https://www.pgatour.com/player/57586/jesper-svensson",
    "https://www.pgatour.com/player/25493/nick-taylor",
    "https://www.pgatour.com/player/51634/sahith-theegala",
    "https://www.pgatour.com/player/33448/justin-thomas",
    "https://www.pgatour.com/player/58168/davis-thompson",
    "https://www.pgatour.com/player/32150/michael-thompson",
    "https://www.pgatour.com/player/57364/michael-thorbjornsen",
    "https://www.pgatour.com/player/52144/braden-thornberry",
    "https://www.pgatour.com/player/30927/brendon-todd",
    "https://www.pgatour.com/player/38991/alejandro-tosti",
    "https://www.pgatour.com/player/35617/martin-trainer",
    "https://www.pgatour.com/player/32333/kevin-tway",
    "https://www.pgatour.com/player/52666/sami-valimaki",
    "https://www.pgatour.com/player/40006/erik-van-rooyen",
    "https://www.pgatour.com/player/27064/jhonattan-vegas",
    "https://www.pgatour.com/player/58619/kevin-velo",
    "https://www.pgatour.com/player/35658/kris-ventura",
    "https://www.pgatour.com/player/54304/karl-vilips",
    "https://www.pgatour.com/player/27770/camilo-villegas",
    "https://www.pgatour.com/player/54607/danny-walker",
    "https://www.pgatour.com/player/25632/jimmy-walker",
    "https://www.pgatour.com/player/48887/matt-wallace",
    "https://www.pgatour.com/player/31113/paul-waring",
    "https://www.pgatour.com/player/27095/nick-watney",
    "https://www.pgatour.com/player/51894/vince-whaley",
    "https://www.pgatour.com/player/50474/tim-widing",
    "https://www.pgatour.com/player/32139/danny-willett",
    "https://www.pgatour.com/player/49964/aaron-wise",
    "https://www.pgatour.com/player/31323/gary-woodland",
    "https://www.pgatour.com/player/08793/tiger-woods",
    "https://www.pgatour.com/player/52374/brandon-wu",
    "https://www.pgatour.com/player/54783/dylan-wu",
    "https://www.pgatour.com/player/54328/norman-xiong",
    "https://www.pgatour.com/player/57366/cameron-young",
    "https://www.pgatour.com/player/45242/kevin-yu",
    "https://www.pgatour.com/player/55454/carl-yuan",
    "https://www.pgatour.com/player/47483/will-zalatoris"
}

players = {
    int(url.split("/")[4]): url.split("/")[5]
    for url in links
}

year = "2025"

for player_id, player_name in players.items():
  # GraphQL query
  query = {
      "operationName": "PlayerProfileStatsFullV2",
      "variables": {
          "playerId": player_id,
      },
      "query": """
      query PlayerProfileStatsFullV2($playerId: ID!) {
        playerProfileStatsFullV2(playerId: $playerId) {
          playerProfileStatsFull {
            stats {
              statId
              title
              value
              rank
              aboveOrBelow
              supportingStat {
                description
                value
              }
              supportingValue {
                description
                value
              }
            }
          }
        }
      }
      """
  }

  # Send request
  response = requests.post(url, headers=headers, json=query)
  data = response.json()

  try:
      stats_section = data.get("data", {}).get("playerProfileStatsFullV2", {})
      stats_list = stats_section.get("playerProfileStatsFull")

      if not stats_list or not isinstance(stats_list, list):
          raise ValueError("Missing or invalid 'playerProfileStatsFull'")

      stats = stats_list[0].get("stats", [])
  except Exception as e:
      print(f"Failed to extract stats: {e}")
      stats = []

  if stats:
      df = pd.DataFrame([{
          "Stat Title": s.get("title"),
          "Value": s.get("value"),
          "Rank": s.get("rank"),
          "Above/Below": s.get("aboveOrBelow", ""),
          "Supporting Stat": f"{s['supportingStat']['description']}: {s['supportingStat']['value']}" if s.get("supportingStat") else "",
          "Supporting Value": f"{s['supportingValue']['description']}: {s['supportingValue']['value']}" if s.get("supportingValue") else ""
      } for s in stats])

      pd.set_option("display.max_rows", None)
      pd.set_option("display.max_columns", None)
      pd.set_option("display.width", None)
      pd.set_option("display.max_colwidth", None)

      # Optional: save to CSV
      df.to_csv(f"./golf_player_stats/{player_name}_stats_{year}.csv", index=False)
  else:
      print("No stats found.")
