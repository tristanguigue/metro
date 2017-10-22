��    g      T  �   �      �  �   �  �  �	  ?  v  }   �  -  4  2   b     �  4   �  	   �  �   �  �  �  �   '          2     ;     V     _     g     y  
   �     �     �     �  �   �  :   n  ^  �            {     �   �  �   �     M  /   a  U   �     �     �  ?   �     8     K     _     e  �   |  �  c  E       S  Q   g     �  9   �  +     �   >          !     %  M   3     �     �     �     �  
   �     �     �  M   �  2   B   2   u   �   �   ?   k!  �   �!    V"  �   _#     $  "   &$     I$  `  L$     �%  	   �%     �%  V   �%     7&  ^   E&  �   �&     ['  �   a'  \  �'  �   N)     �)     	*      *  >   %*  �   d*     _+     u+     x+     |+  �   �+  )   �,  /   �,  H   �,     --  	   9-      C-  /   d-      �-  q  �-  �   '/  �  0  �  �1  �   A3  i  �3  @   95     z5  5   �5     �5  �   �5  �  Q6  %  *8  $   P9     u9  !   ~9  	   �9     �9     �9     �9  
   �9  %   �9     �9     :  �   :  J   �:  Y  ;  	   l<     v<  �   y<  �   =  �   �=     �>  8   �>  Z   6?     �?     �?  Z   �?      @     @     6@     <@    Z@  B  mA  �  �B     CE  X   ZE  0   �E  H   �E  9   -F  �   gF     ;G     XG     ]G  L   nG     �G  	   �G     �G     �G      H     H     (H  T   BH  ;   �H  A   �H  �   I  [   �I  �   ?J  F  �J  �   'L     M  $   M     CM  .  FM  %   uN  
   �N     �N  e   �N     O  d   3O  �   �O     jP  x   nP  C  �P    +R     .S      IS     jS  D   oS  �   �S  '   �T     �T     �T     �T  �   �T  /   �U  3   �U  C   .V     rV     �V  (   �V  =   �V  +   �V     f            R              E   /             e       *           c   2          0   X                     4   
       a   \      3   6   #   8   W       G   ]   ?   A       ^   D   Z                   H   9       L   F   -   Q   .           "   >   M       ,          )   O   '       `   ;   b              1   :      V   I      P          @   <      K      [   C              N   (   !   T   d   g       Y             $   %   J           _   =   5       B          &         U   	      +      S      7               For lines with small ridership such as 3b and 7b the time difference is very small as removing a station doesn't impact many people. In this case it is the financial argument that is the most relevant to justify their closure.  However travelling accross Paris with the metro can be slow due to the density of stations: the average distance between stations is 570 meters compared to 1200m for the world average and the average commercial speed across the network is only 27km/h. As a consequence trains almost never reach their maximum speed. For example it takes 52 minutes on line 9 to cover the 19.5km between Pont de Sèvre and Montreuil compared to 29 minutes for the Victoria line in London for 21km.  Paris metro is over a hundred years old and the first lines were built when the city extended little behind its administrative border. Today Paris is a metropolis of over 12 millions inhabitants, among those only 2.2m live in the city proper. The metro has expanded into its suburbs and further expansions are planned.  To calculate the time difference per person we assume an average of 100 trips accross the network per person (Source : GART) A station is considered very relevant if it is used by many passengers, is far from other stations and have little through traffic. Vice-versa a station is considered not relevant if few passengers use it, it is close to other stations and many passengers travel through the station without alighting. Allow faster travel between Paris and its suburbs. Analysis And the number of secondary passengers alighting is: Arguments As an example, the most used section is between Réaumur-Sébastopol and Etienne Marcel on line 4 with an estimated 113 millions passenger per year travelling between those 2 stations every year. As the number of transfer passenger and the occupancy of the train depends on each other we first calculate the number of passenger that would transfer at every station without actually using this data and in a second run include the pre-calculated incoming transfer passengers. Optimally we would run this until we reach convergence however is this project we have ran a single iteration. Based on this data, the most relevant stations are located outside of Paris city as expected. The least relevant stations are located in the center of Paris where the ridership is high and the stations sometimes very close to each other. Bottom 10 stations to remove Branches Calculating Passenger Flow Capacity Contact Counter arguments Density Discussion Effect of Station Removal Efficiency and Reliability English Evaluating stations' relevance based on their distance to other stations, the number of passengers using this station and the ridership on this section of the line. Focus maintainance and improvements on remaining stations. For each line, we navigate the routes taken by the train starting from one of the termini. At each station we estimate the number of passenger that who would board and alight the train, we then update the simulated occupacy of the train. The initial occupancy is 0. One the first users have boarded the train the occupancy between station 0 and 1 is: French From Go along with expansion of metro network in the suburbs (line 4, 12, 14) and Grand Paris Express (line 11, 15, 16, 17, 18). If the station have multiple lines we split the entries between each line according to the global weight of the line given by the total passengers per year coming from another public dataset. Similarly the number of passenger alighting is given by: In this project we study the effect of removing each station in terms of the gain or loss of time induced on the users based on the simulation of the ridership in all the sections of the network. Least used sections Least used segments (excluding lines 3b and 7b) Let the metro play its role as a structuring network for Paris and the inner suburbs. Line Methodology More efficient and reliable service, removing potential delays. Most used sections Network Development Notes Paris Metro Simulation Paris is one of the densest cities in the world, which justify having a higher density of station. This is a valid argument however a balance has to be found for the network to be useful for both the city and the suburb residents. Paris metro is one of the densest in the world: the average distance between stations is 570 meters. Travelling accross Paris can therefore be slow due to the high number of stations: the average commercial speed across the network is only 27km/h. As an example it takes 52 minutes on line 9 to cover the 19.5km between Pont de Sèvre and Montreuil which makes this option unattractive compared to other transportation means. Paris metro uses small train for historical reasons and does not have enough capacity to use existing lines for transporation at the scale of the metropolis. This is also true, which is why the Grand Paris Express lines are being built. However it should be possible to use the historical network beyond its current use for short-trip within Paris. The RER and Grand Paris Express alone cannot cater the 12 millions inhabitans of  greater Paris, the existing network should be able to contribute to serve the densily populated inner suburbs as long as travel times stay acceptable. Passengers (m/year) Possibility to convert closed stations in cultural venues, restaurants, commerce. Promote public transport usage Reduce fatigue and marginalisation of suburbs' residents. Reducing historic inner city/suburbs split. Removing a station changes the relevance of neighbour stations, therefore to know which stations are the less relevant we would need to greedily remove the least relevant station and re-run the simulation. Ridership Simulation See Side Benefits Simulating the flow of passenger in every section of the Paris metro network. Simulation of Ridership Some Station Stations Revelance Statistics The code is available on The discussion is open The factor 2 accounts for both entries and exits which we assume to be equal. The number of primary passengers alighting is now: The time lost when removing station i is given by: The transfers between lines are not taken into account in the entries given by the public data, so to have a better picture of the flow of passengers we need to simulate transfers between lines. This indicates where to expect the most crowds on a given line. This is a simulation of the average yearly passengers travelling between each station of the Paris metro network based on the yearly entries given for each station by the This map shows the time gained or lost by all the network users combined when removing a given station. This is calculated by substracting the time lost by users who have to walk to the next station from the time gained by users in the train that do make the stop. This project is meant to open the discussion on a way to make Paris metro more efficient and provide a new point of view on the topic based on data. Suggestions are welcome! Time Gained (years/year) Time Gained Per Person (mins/year) To To do so we split the traffic into primary and secondary traffic. We allow a single transfer to reduce complexity. The primary traffic is given by the passengers coming from the street or another transportation mean, the secondary traffic is given by the passgengers coming from another line. The number of passenger boarding the train is now given by: Top 10 stations to remove Transfers Urban Cohesion We do not consider transfer and end stations as they form the backbone of the network. What is this? When a line has multiple branches we split the traffic according to the weight of each branch. When removing a station i we calculate the time gained by the passengers as the sum of the occupancy in the incoming and outcoming edges times the time gained when avoiding the stop: Where Where \(e_0\) is the number of passengers that have entered at station 0 and this is given by the public dataset. In the general case, we have: Where \(wt\) is the weight taking into account future transfers, in particular we add to the weight of each transfer station the total weight of the other lines multiplied by a transfer coefficient. The transfer coefficient is chosen such as to keep at total transfers to entries ratio corresponding to data given by the RATP for specific stations. Where we split the station entries according to the 'weight' of the remaining stations in each direction, by weight we mean the cumulated entries of those stations: Why does this matter? Why removing stations? With With \(n_{i}^{in}\) the number of passenger boarding given by: With only 5 RER lines to server the greater Paris, many suburbs resident prefer using their car generating pollution and traffic jams. A faster, more reliable and expended metro network would make it easier to switch from private to public transport. You can contact me at at dot for explanations have been made to remove stations from the network but all were based on the sole number of entries and distance to the nearest station without considering the ridership on each section of the line which influences the overall time gain in the network. is the number of line crossing at station is the transfer coefficient as described above. is the weight of the line given by the cumulated weight of the stations. methodology proposals the acceleration of the train in the cruising speed of the train of that line in the deceleration of the train in Project-Id-Version: PACKAGE VERSION
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2017-10-22 19:35+0100
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language-Team: LANGUAGE <LL@li.org>
Language: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=n == 1 ? 0 : 1;
 Pour les lignes très peu fréquentées comme la 3b et la 7b, la différence en temps est très petite car leur suppression impacte peu de gens. Dans ce cas, l'argument financier est plus pertinent pour justifier leur fermeture. Mais traverser Paris en métro est particulièrement lent du à la densité historique de stations: la distance moyenne entre stations est de 570 mètres comparé à 1200 en moyenne dans le monde. Par conséquence les trains n'atteignent pratiquement jamais leur vitesse de pointe. Par exemple, il faut 52 minutes pour parcourir les 19.5km de la ligne 9 comparé à 29 minutes pour les 21km de la ligne Victoria à Londres. Le métro de Paris fut construit avec l'objectif de relier les différents arrondissements de la capitale qui s'étendait peu au delà de ses limites administratives. Aujourd'hui la métropole parisienne compte plus de 12 millions d'habitants dont 2.2 millions seulement vivent dans Paris intra-muros. Le métro s'est depuis étendu à la proche banlieue et de nouveau prolongements sont prévus. Pour calculer le gain de temps par personne, on assume une moyenne de 100 déplacements par personne et par an sur le réseau (Source: GART)  Une station est considérée comme pertinente si elle a un grand nombre de passagers entrants, elle est loin d'autres stations et il y a peu de trafic qui la traverse. Vice-versa une station est considérée comme peu pertinente si peu de passagers l'utilisent, elle est proche d'une autre station et il y a un trafic important qui la traverse sans y descendre. Permettre des connexions plus rapide entre Paris et sa banlieue. Analyse Et le nombre de passagers secondaires descendant est: Argumentation Par exemple, le tronçon le plus utilisé est Réaumur-Sébastopol - Etienne Marcel sur la ligne 4 avec 113 millions de passagers par ans. Comme le nombre de passagers en transfert et la fréquentation du train dépendent l'un de l'autre on calcul dans un premier temps le nombre de passagers qui effectueraient le transfert à chaque station sans le prendre en compte. Dans un second temps on inclut le nombre de passagers entrant en transfert précalculé. Idéalement on itererait jusqu'à atteindre la convergence du trafic. Dans ce projet néanmoins nous n'utilisons qu'un seule itération de ce processus. En utilisant cette grille de lecture on peut voir que les station les plus pertinents sont situés en banlieue ou les stations sont plus éloignées alors que les moins pertinentes se trouvent dans Paris intra-muros ou les lignes sont très fréquentées et les stations parfois très proches. Les 10 stations les plus pertinentes Branches Calculation des flux de passagers Capacité Contact Contre-arguments Densité Discussion Effet de la suppression d'une station Efficacité et fiabilité Anglais Évaluer la pertinence des stations en se basant sur le nombre d'entrants, la distance à la station la plus proche et la fréquentation sur cette section de la ligne. Focaliser la maintenance et les améliorations sur les stations restantes. Pour chaque ligne, la fréquentation est calculée à partir de chaque terminus. À chaque station le nombre de passagers descendants est estimé, la fréquentation est alors mise à jour. La fréquentation initiale est 0. Une fois prise en compte les passagers entrants au terminus la fréquentation de la section entre les station 0 et 1 est:  Français De Accompagner le dévelopement du réseau en banlieue (prolongement ligne 4, 11, 12 et 14) et le Grand Paris Express (ligne 15, 16, 17, 18). S'il y a plusieurs lignes à une même station, les entrants sont divisés entre chacune des lignes utilisant pour le poids global de chaque ligne leur fréquentation annuelle. De même manière le nombre de passagers descendant est donné par: Dans ce projet nous étudions l'effet de supprimer chacune des stations en terme de gain ou perte de temps induite sur tout les utilisateurs et en utilisant la simulation de la fréquentation dans chacune des sections du réseau. Sections les moins utilisées Sections les moins utilisées (excluant lignes 3b et 7b) Laisser le métro jouer son rôle de réseau structurant pour Paris et la proche banlieue. Ligne Méthodologie Assurer un service plus efficace et fiable en supprimant une source de délais potentiels. Sections les plus utilisées Dévelopement du réseau Notes Simulation du métro de Paris Paris est une des villes les plus dense au monde ce qui justifie d'avoir une densité plus élevé de stations. C'est un argument valide, le plus important étant de trouver le juste équilibre entre les déplacements intra-muros et ceux Paris-banlieue ou banlieue-banlieue. Le métro de Paris est un des plus dense au monde: la distance moyenne entre stations est de 570 mètres. Traverser Paris est par conséquence particulièrement long: la vitesse moyenne du réseau est de seulement 27km/h. Par exemple parcourir les 19.5km de la ligne 9 prend 52 minutes rendant cette option peu attractive. Pour des raisons historiques, le métro de Paris utilise un matériel de petit gabarit qui n'a pas une capacité suffisante pour être utilisé comme un réseau structurant à l'échelle de la métrople. Cela est aussi vrai et une des raisons pour laquelle le Grand Paris Express est en construction. Mais le réseau historique a aussi un rôle à jouer dans la desserte de la banlieue parisienne, le RER et le Grand Paris Express seuls ne peuvent déservir les 12 millions d'habitants du Grand Paris. Le métro existant doit pouvoir contribuer au maillage de la petite courronne densément urbanisée à condition que les temps de trajets soit accéptables. Passagers (million/an) Possibilité de convertir les stations fermées en venues culturelles, restaurants, etc. Promouvoir l'utilisation des transports publics. Réduire la fatigue et la marginalisation des résidents de la banlieue. Réduire le fossé historique entre Paris et sa banlieue. Supprimer une station change la pertinence de stations voisines par conséquence pour savoir quelle sont les stations les moins pertinentes il faudrait les supprimer une par une et refaire marcher la simulation. Simulation de fréquentation Voir Autres avantages Une simulation du flux de passagers dans chaque tronçon du métro de Paris. Fréquentation par section Certaines Station Pertinence des stations Statistiques Le code est disponible sur La discussion est ouverte Le facteur 2 prends en compte les entrées et sorties que l'on assume être égales. Le nombre de passagers primaires descendant est maintenant: Le temps perdu lorsque l'on supprime la station i est donné par: Les transferts entre lignes ne sont pas pris en compte dans les entrants du jeu de données public. Pour avoir une meilleur idée du flux de passager, il nous faut simuler les transferts entre les lignes.  Cela permet de prédire les sections ou l'affluence sera la plus importante sur le réseau. Ceci est une simulation du nombre moyen de passagers entre chaque station de métro calculé en utilisant le nombre d'entrants annuels par station donné par la Cette infographie montre le temps gagné ou perdu par l'ensemble des utilisateurs du réseau lorsqu'une station donnée est supprimée. Ceci est calculé en soustrayant le temps perdu par les passagers qui doivent marcher jusqu'à la station la plus proche au temps gagné par les passagers qui ne s'arrête pas à la station. L'idée de ce projet était d'illustrer une possibilité d'améliorer l'éfficacité du réseau de métro en respectant l'intérêt général et en se basant sur des données publiques.  Vos suggestions sont les bienvenues! Gain de temps (ans/an) Gain de temps par personne (mins/an) À Pour ce faire, nous divisons le trafic entre trafic primaire venant directement de la rue ou d'un autre moyen de transport et le trafic secondaire venant d'une autre ligne. Pour simplifier nous ne considérons qu'un seul transfert possible. Le nombre de passager qui embarque est maintenant donné par: Les 10 stations les moins pertinentes Transferts Cohésion urbaine Les stations de transfert et terminus ne sont pas considéré car elle forme le squelette du réseau. Qu'est ce que c'est? Lorsqu'une ligne a plusieurs branches, le trafic est divisé en fonction du poids de chaque branche. Lorsque la station i est supprimé, le temps gagné par les passagers est donné par la somme de la fréquentation des tronçons entrants et sortants multiplié par le temps gagné en ne marquant pas l'arrêt: Où Ou \(e_0\) est le nombre de passagers entrants au terminus (station 0) qui est public. Dans le cas général cela donne: Ou \(wt\) est le poids prenant en compte les futurs transferts c'est à dire qu'à chaque station de transfert on ajoute le poids des lignes adjacentes mutliplié par un coefficient de transfert. Le coefficient de transfert est choisi de manière à conserver le ratio de entrants/transfert donné pour certaines stations.  Les entrants sont divisé entre ceux prenant la direction considérée et ceux prenant la direction opposée en fonction du poids des stations restantes dans chaque direction. Par poids on sous-entends le nombre cumulé d'entrants des stations considérées. Pourquoi est-ce important? Pourquoi supprimer des stations? Avec \(n_{i}^{in}\) étant le nombre de passagers embarquants donné par: Avec seulement 5 lignes de RER pour désservir le grand Paris, de nombreux résident de banlieue préfèrent utiliser leur voiture, un métro plus rapide et plus éfficace serait plus attractif et pourrait contribuer à réduire la pollution. Vous pouvez me contacter par courriel:  arobase point pour plus de détails on été faite en ce sens mais toujours basé uniquement sur le nombre d'entrant dans une station sans considérer la fréquentation de cette section de la ligne qui influence le temps total gagné dans le réseau. est le nombre de ligne présentes à la station est le coéfficient de transfert décrit ci-dessus. est le poids de la ligne donnée par le poids cumulé des stations. méthodologie propositions est l'accélération du train donnée en est la vitesse de pointe du train sur cette ligne exprimé en est la déccélération du train donnée en 