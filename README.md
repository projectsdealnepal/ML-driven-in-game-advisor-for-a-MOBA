# ML-driven-in-game-advisor-for-a-MOBA
The main idea of the software is that it is a tool that will be aimed at novice players as they are the ones who would require such a simple guidance tool. The users simply need to download it from the Steam Market and run it at the same time as their games. Before using it the player should connect their Steam account to the tool to establish connection and select from a few predefined positions of where on the screen should the tips show up. Therefore, the tool would then need to be installed and run parallel with the game, pushing in these notifications. If authentication is needed a simple email and password is enough. In terms of the GUI it could be a very simple one basic one, coming with some frontend library as it won’t have any visual elements. To get data from the actual game it needs an API connection with the following key parameters. Some key parameters to identify would be the game of the user, the amount of gold they have, role, lane, already existing items, game time, already purchased items, used hero in order to be able to provide continuous item suggestions to the player. The tool can just provide a simple popup window with the suggested items and item description on the bottom confirming or declining if this suggestion is a good one. Also, a checkbox is needed to disable the suggestions, in case the player finds the tool disturbing. Also, the model can first be trained with some parsed matches. In order to receive feedback from these users, a simple yes-or-no type of reaction would be possible to provide in terms of the usefulness of each and every individual suggestion. As a bonus, this would also help with the further training of the software. Moreover, at the end of each match, the player would receive the option to fill out a survey of a few questions to evaluate the overall usefulness of the provided solution. The survey will consist of not more than 5 questions. In order to double check the overall positive or negative ratings of users, the outcome of games could be used as a control variable, so a summary of the win rates would be needed as well.
# API key for accessing https://docs.opendota.com/# -CD851130257D6C98D760E9CF00CABF6A 
