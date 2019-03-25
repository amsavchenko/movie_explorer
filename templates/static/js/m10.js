function create () 
{
    var el = document.createElement("p");        
    var text = document.createTextNode("Запрос на сервер отправлен, ожидайте ответ...");       
    el.appendChild(text);                                
    document.body.appendChild(el);  
}

function autocomplete(inp, arr) {
    var currentFocus;
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(a);
        count_of_add = 0
        for (i = 0; i < arr.length; i++) {
          if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase() && count_of_add < 10 ) {
            b = document.createElement("DIV");
            b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
            b.innerHTML += arr[i].substr(val.length);
            b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
            b.addEventListener("click", function(e) {
                inp.value = this.getElementsByTagName("input")[0].value;
                closeAllLists();
            });
            a.appendChild(b);
            count_of_add = count_of_add + 1;
          }
        }
    });
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
          currentFocus++;
          addActive(x);
        } else if (e.keyCode == 38) { 
          currentFocus--;
          addActive(x);
        } else if (e.keyCode == 13) {
          e.preventDefault();
          if (currentFocus > -1) {
            if (x) x[currentFocus].click();
          }
        }
    });
    function addActive(x) {
      if (!x) return false;
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
          x[i].parentNode.removeChild(x[i]);
        }
      }
    }
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
  }
  
  var countries = ['Minority Report (2002)',
  'Maquia: When the Promised Flower Blooms',
  'Guardians of the Galaxy Vol. 2',
  'Ralph Breaks the Internet',
  'Skyscraper',
  'Overlord',
  'Fantastic Beasts and Where to Find Them',
  'Edward Scissorhands (1990)',
  'Red Sparrow',
  'Hunter Killer',
  'Short Cuts (1993)',
  'The Hunger Games: Mockingjay - Part 1',
  'Pariyerum Perumal',
  'The Predator',
  'Night School',
  'Jurassic World: Fallen Kingdom',
  'The Exorcist (1973)',
  'Rounders (1998)',
  'Kramer Vs. Kramer (1979)',
  'Harry Potter and the Prisoner of Azkaban',
  'Rango (2011)',
  'Flight (2012)',
  'The Fifth Element (1997)',
  'The Avengers',
  'Deadpool',
  'Harry Potter and the Deathly Hallows: Part 1',
  'Spectre',
  'Replicas',
  'Incendies (2010)',
  'Mandy',
  'Traffic (2000)',
  'Death Race 4: Beyond Anarchy',
  'Hereditary',
  "The Girl in the Spider's Web",
  'Inception',
  'Doctor Strange',
  'The Darkest Minds',
  'War for the Planet of the Apes',
  'Exodus: Gods and Kings',
  'Inglourious Basterds',
  'Pirates of the Caribbean: On Stranger Tides',
  'The 12th Man',
  'Million Dollar Baby (2004)',
  'The Other Side of the Wind',
  'Blindspotting',
  'Bohemian Rhapsody',
  'Female War: A Nasty Deal',
  'Rambo: First Blood Part II',
  'Bad Times at the El Royale',
  'The Purge',
  'Gone Girl',
  'Deadpool 2',
  'The Spy Who Dumped Me',
  'Stardust (2007)',
  'Christopher Robin',
  'The Purge: Election Year',
  'Mission: Impossible - Rogue Nation',
  'River Runs Red',
  'The Aviator (2004)',
  'Django Unchained',
  'The Purge: Anarchy',
  'Aladdin (1992)',
  'Alien: Covenant',
  'Mamma Mia! Here We Go Again',
  'The First Purge',
  '4 Months, 3 Weeks and 2 Days (2007)',
  'Harry Potter and the Order of the Phoenix',
  'Best in Show (2000)',
  'The Shape of Water',
  'The Lord of the Rings: The Two Towers (2002)',
  'Sorry to Bother You',
  'The Greatest Showman',
  'The Holiday Calendar',
  'Hotel Artemis',
  'Interstellar',
  'Sideways (2004)',
  'Split',
  'The Dark Knight',
  'BlacKkKlansman',
  'The Dark Knight Rises',
  'Shutter Island (2010)',
  "Ocean's Eleven",
  'Raising Arizona (1987)',
  'The Lord of the Rings: The Two Towers',
  'The Wolf of Wall Street',
  'Ant-Man',
  "Harry Potter and the Philosopher's Stone",
  'A Star Is Born',
  "Ocean's Eight",
  'Star Wars: The Force Awakens',
  'The Scorpion King: Book of Souls',
  'Annihilation',
  'First Blood',
  'Venom',
  'The Artist (2011)',
  'Billy Elliot (2000)',
  'Jurassic World',
  'Fifty Shades Freed',
  'Thor',
  'Spirited Away',
  'Black Panther',
  'The Kissing Booth',
  'Hotel Transylvania 2',
  'Avengers: Infinity War',
  'Ready Player One',
  'Kin',
  'The Imitation Game',
  'Pulp Fiction',
  'Blue Jasmine (2013)',
  'Siberia',
  "Ender's Game",
  'The Nutcracker and the Four Realms',
  'Papillon',
  'The Equalizer 2',
  'Pirates of the Caribbean: Dead Men Tell No Tales',
  "It's Christmas, Eve",
  'The Miseducation of Cameron Post',
  "Pirates of the Caribbean: At World's End",
  'Johnny English Strikes Again',
  'Fight Club',
  'Planes, Trains and Automobiles (1987)',
  'The Silence of the Lambs (1991)',
  'Searching',
  'Sunshine (2007)',
  'Harry Potter and the Deathly Hallows: Part 2',
  'Once Upon a Time in the West (1968)',
  'Milk (2008)',
  'Strangers on a Train (1951)',
  'Mad Max: Fury Road',
  'Coco',
  'Batman v Superman: Dawn of Justice',
  'Zoe',
  'Forrest Gump',
  'The Maze Runner',
  'Blade Runner 2049',
  'Whiplash',
  'Mission: Impossible',
  'Aan Devathai',
  'Hotel Transylvania 3: Summer Vacation',
  'The Hobbit: The Battle of the Five Armies',
  'Tomb Raider',
  'The Hurt Locker (2008)',
  'The Godfather',
  'A Quiet Place',
  'Maze Runner: The Death Cure',
  'The Seven Deadly Sins: Prisoners of the Sky',
  'An Education (2009)',
  'Den of Thieves',
  'The Wave (2008)',
  'Touch of Evil (1958)',
  'The Hobbit: An Unexpected Journey',
  'Alpha',
  'Pacific Rim: Uprising',
  'Thor: Ragnarok',
  'Kamen Rider Amazons The Movie: The Final Judgement',
  'Mile 22',
  'Incredibles 2',
  'Spider-Man: Homecoming',
  'Logan',
  'Blade Runner',
  'The Bourne Ultimatum (2007)',
  'The Piano (1993)',
  'The Equalizer',
  'The Legend of Drunken Master (1994)',
  'Batman (1989)',
  'Chocolat (2000)',
  'Smallfoot',
  'In the Heat of the Night (1967)',
  'A-X-L',
  'The Grapes of Wrath (1940)',
  'Terminal',
  'Star Wars',
  'The Way Way Back (2013)',
  'The Lord of the Rings: The Fellowship of the Ring',
  'Three Billboards Outside Ebbing, Missouri',
  'Avengers: Age of Ultron',
  'Guardians of the Galaxy',
  'Overboard',
  'Mission: Impossible - Ghost Protocol',
  'Pirates of the Caribbean: The Curse of the Black Pearl',
  'Lost in Translation (2003)',
  'Wonder Woman',
  'Creed II',
  "Breakfast at Tiffany's (1961)",
  "To All the Boys I've Loved Before",
  'Upgrade',
  'X-Men: Apocalypse',
  'Goosebumps 2: Haunted Halloween',
  'Crazy Rich Asians',
  "Pirates of the Caribbean: Dead Man's Chest",
  'X-Men: Days of Future Past',
  'The Impossible (2012)',
  'The Nun',
  'Sicario: Day of the Soldado',
  'Justice League',
  'Harry Potter and the Half-Blood Prince',
  'Ant-Man and the Wasp',
  'First Man',
  'The Mission (1986)',
  'The Hate U Give',
  'Trainspotting (1996)',
  'Batman Begins',
  'Big Hero 6',
  'Finding Nemo',
  'Game Night',
  'Dawn of the Planet of the Apes',
  'In a Relationship',
  'Billy: The Early Years',
  'Terminator Genisys',
  'Beverly Hills Cop (1984)',
  'Insurgent',
  'Down by Law (1986)',
  'Hangover (2014)',
  'Rambo III',
  'Thor: The Dark World',
  'Halloween',
  'Harry Potter and the Chamber of Secrets',
  'Gosford Park (2001)',
  'Double Indemnity (1944)',
  'The Incredibles',
  'Widows',
  'Now You See Me 2',
  'Adrift',
  'Fury',
  'Star Wars: The Last Jedi',
  'Night at the Museum: Secret of the Tomb',
  'Iron Man 3',
  'Kingsman: The Secret Service',
  'Solo: A Star Wars Story',
  'Gladiator (2000)',
  'Eastern Promises (2007)',
  'Three Days of the Condor',
  'The Godfather: Part III (1990)',
  'The Fighter (2010)',
  "It's a Wonderful Life (1946)",
  'The Thinning: New World Order',
  'Vacation (2015)',
  'On the Waterfront (1954)',
  'Rampage',
  'The Lion King (1994)',
  'The Shawshank Redemption',
  'Following (1998)',
  'Time Freak',
  'Hostiles',
  'Twilight',
  'House of Sand and Fog (2003)',
  'The Grinch',
  'The Meg',
  'Pulp Fiction (1994)',
  'Bird Box',
  'Good Bye, Lenin! (2003)',
  'Synecdoche, New York (2008)',
  'The Matrix',
  'Mission: Impossible - Fallout',
  'Fantastic Beasts: The Crimes of Grindelwald',
  "One Flew Over the Cuckoo's Nest"]

  autocomplete(document.getElementById("myInput"), countries);