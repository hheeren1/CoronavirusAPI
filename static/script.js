if(window.location.protocol != 'https:') {
    location.href =   location.href.replace("http://", "https://");
}
if (window.location.href.indexOf("?") > -1) {
  document.location.href="/";
}

var searchForm = document.getElementById('search');
var searchButton = document.getElementById('search-button');
var searchInput = document.getElementById('search-input');
var resultsContainer = document.getElementById('result');

var resultsElements = {
	title: resultsContainer.querySelector('h1'),
	description: resultsContainer.querySelector('.result__description'),
	image: resultsContainer.querySelector('.result__image'),
	table: resultsContainer.querySelector('.result__table'),
	source: resultsContainer.querySelector('.result__source'),
	attribution: resultsContainer.querySelector('.result__attribution')
}


search.addEventListener('submit', function(e) {
    searchButton.classList.add('active');
    resultsContainer.classList.add('loading');
	sendrequest(searchInput.value);
	e.preventDefault();
});

function sendrequest(country) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', window.location.href+country, true);
    xhr.responseType = 'json';
    xhr.send();
    xhr.onload = function() {
      console.log(xhr.response)

        var result = xhr.response;
        if(result != null){
            submit(result.Country,result.Flag,result.Cases,result.Deaths,result.Recovered,result.Date,result.CasesToday,result.DeathsToday)
          }
    }
  
}

function submit(country,img,cases,deaths,recovered,date,casestoday,deathstoday) {
    if(casestoday != 0)
    {
      cases = cases+"\xa0\xa0(Today: "+casestoday+")"
    }
    if(deathstoday !=0)
    {
      deaths=deaths+"\xa0\xa0(Today: "+deathstoday+")"
    }

    var dataTable = {
        cases: {label:"Cases",value: cases},
        deaths: {label:"Deaths",value: deaths},
        recovered: {label:"Recovered",value:recovered}}
    

    if (img === undefined){
        resultsElements.table.classList.add('hidden');
        resultsContainer.classList.add('result--no-image');
        resultsElements.description.innerHTML = "The country '"+country+"' is wrong.<br>Please type the country name properly<br><br>Try something like Morocco, USA, France, Italy...";
        resultsElements.title.textContent = "ERROR";
    }else{
        resultsContainer.classList.remove('result--no-image');
        resultsElements.image.src = '';
        resultsElements.image.src = img;
        resultsElements.description.innerHTML = "Coronavirus statistics of '"+country+"' <br><br>"+"Last Updated :<br>"+date;
        resultsElements.title.textContent = country;
    }

    if (cases !== undefined && deaths !== undefined && recovered !== undefined)
    {
        
    var hiddenClass = 'hidden';
    resultsElements.table.classList.remove(hiddenClass);
    var tableFragment = document.createDocumentFragment();

    for (item in dataTable) {
    var row = document.createElement('tr');
    row.className = 'table__row';

    var nameCell = document.createElement('td');
    var valueCell = document.createElement('td');
    nameCell.className = valueCell.className = 'table__cell';
    nameCell.textContent = dataTable[item].label;
    valueCell.textContent = dataTable[item].value;

    row.appendChild(nameCell);
    row.appendChild(valueCell);
    tableFragment.appendChild(row);
    }
    resultsElements.table.innerHTML = '';
    resultsElements.table.appendChild(tableFragment);
    }

    searchButton.classList.remove('active');
    resultsContainer.classList.remove('loading');
    searchInput.value = '';
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
        for (i = 0; i < arr.length; i++) {
          if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
            b = document.createElement("DIV");
            b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
            b.innerHTML += arr[i].substr(val.length);
            b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
            b.addEventListener("click", function(e) {
                inp.value = this.getElementsByTagName("input")[0].value;
                closeAllLists();
            });
            a.appendChild(b);
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
  
  var countries = ["World","USA","Spain","Italy","Germany","France","Iran","UK","Turkey","Belgium","Switzerland","Netherlands","Canada","Brazil","Portugal","Austria","Russia","S. Korea","Israel","Sweden","India","Ireland","Norway","Australia","Chile","Denmark","Poland","Czechia","Japan","Romania","Peru","Ecuador","Pakistan","Malaysia","Philippines","Saudi Arabia","Indonesia","Mexico","Luxembourg","Serbia","UAE","Finland","Panama","Qatar","Thailand","Dominican Republic","Colombia","Ukraine","Singapore","South Africa","Belarus","Greece","Argentina","Egypt","Iceland","Algeria","Croatia","Moldova","Morocco","New Zealand","Estonia","Iraq","Hungary","Slovenia","Lithuania","Kuwait","Hong Kong","Armenia","Azerbaijan","Bahrain","Bosnia and Herzegovina","Kazakhstan","Cameroon","Slovakia","Diamond Princess","North Macedonia","Tunisia","Bulgaria","Uzbekistan","Latvia","Lebanon","Andorra","Cyprus","Costa Rica","Afghanistan","Cuba","Oman","Uruguay","Ivory Coast","Burkina Faso","Bangladesh","Albania","Niger","Honduras","Taiwan","Ghana","Jordan","Réunion","Channel Islands","Malta","San Marino","Mauritius","Kyrgyzstan","Nigeria","Bolivia","Palestine","Senegal","Vietnam","Montenegro","Georgia","DRC","Guinea","Mayotte","Sri Lanka","Isle of Man","Kenya","Faeroe Islands","Venezuela","Martinique","Djibouti","Guadeloupe","Brunei ","Paraguay","Guatemala","Gibraltar","Cambodia","El Salvador","Rwanda","Trinidad and Tobago","Madagascar","Mali","Monaco","French Guiana","Aruba","Liechtenstein","Togo","Barbados","Ethiopia","Jamaica","Congo","Uganda","French Polynesia","Sint Maarten","Bermuda","Cayman Islands","Macao","Gabon","Bahamas","Zambia","Guyana","Guinea-Bissau","Eritrea","Tanzania","Saint Martin","Liberia","Haiti","Myanmar","Benin","Libya","Angola","Antigua and Barbuda","Syria","Maldives","Equatorial Guinea","New Caledonia","Mozambique","Dominica","Fiji","Laos","Mongolia","Namibia","Sudan","Curaçao","Saint Lucia","Botswana","Somalia","Grenada","St. Vincent Grenadines","Eswatini","Zimbabwe","Chad","Greenland","Saint Kitts and Nevis","Seychelles","Belize","Suriname","MS Zaandam","Malawi","Nepal","Montserrat","Turks and Caicos","CAR","Vatican City","Cabo Verde","Mauritania","Nicaragua","Sierra Leone","St. Barth","Bhutan","Falkland Islands","Gambia","Sao Tome and Principe","South Sudan","Western Sahara","Anguilla","British Virgin Islands","Burundi","Caribbean Netherlands","Papua New Guinea","Timor-Leste","Saint Pierre Miquelon","Yemen","China"];
  autocomplete(document.getElementById("search-input"), countries);
