const processXML = content => {
    var xmlDoc = new DOMParser().parseFromString(content, 'text/xml');

    var issues = xmlDoc.getElementsByTagName("issue");
    for (k=0; k<issues.length; k++){ 

        var volume = $(issues[k]).find("volume").text();
        var number = $(issues[k]).find("number").text();
        var year = $(issues[k]).find("year").text();
        var issue = 'Vol. '+volume+' Núm. '+number+' ('+year+')';

        var articles = issues[k].getElementsByTagName("article");
        for (i=0; i<articles.length; i++){ 
            var titulo = $(articles[i]).find("title").text();
            autores = articles[i].getElementsByTagName("author");
            lista_autores = "";
            for(j=0; j<autores.length; j++){
                givenname = $(autores[j]).find("givenname").text() || "";
                familyname = $(autores[j]).find("familyname").text() || "";
                firstname = $(autores[j]).find("firstname").text() || "";
                middlename = $(autores[j]).find("middlename").text() || "";
                lastname = $(autores[j]).find("lastname").text() || "";
                autor = givenname+' '+firstname+' '+middlename+' '+familyname+' '+lastname;
                lista_autores = lista_autores+autor+"; ";
            }
            fecha = articles[i].getAttribute("date_published");
            var added = lista.row.add([issue, titulo, lista_autores, fecha ]).node();
            $(added).addClass('paper');
            lista.draw();
            var embed = $(articles[i]).find("embed").html();
            paper_list[titulo] = embed;
        }
    }
}