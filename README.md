# TP Opensearch - Romain Delage

## Dataset

Pour ce TP le dataset choisi contient[ Les projets github les plus étoilées jusqu'a 2017 ](https://www.kaggle.com/yamqwe/top-starred-open-source-projects-on-githube).

**[!]** **Je ne me suis rendu compte que trop tard que ce dataset n'est que peu exploitable** **[!]**

**Les requêtes ont était faites avec l'outil  *Insomnia***

Pour rendre le dataset intégrable par la methode *_bulk*, j'ai développé un petit script python automatisant la création du fichier *github.json* contenant toutes les données formaté pour l'importation dans Opensearch avec cette methode. Ce script est présent dans le dossier du projet en tant que *csvtojson.py*

**Ce dataset contient :**
- Le nom du propriétaire du depo
- le nom du depo
- La description du depo
- La date de la dernière mise à jour du depo
- Le langage utilisé
- Le nombre d'étoile du depo
- Les tags du depo
- L'url github du depo

Le mapping *github_mapping.json* indique que chaque champs est de type texte.

Le création de l'index ce fait avec la requête **PUT** suivnate:

*@PUT*
```https
https://localhost:9200/repositories?pretty
```

Ce qui renvoit:
```json
{
	"acknowledged": true,
	"shards_acknowledged": true,
	"index": "repositories"
}
```

Nous avons donc désormais un index "*repositories*"

Ensuite, nous importons le mapping présent dans *github_mapping.json* avec la requête **PUT** suivante

*@PUT*
```https
https://localhost:9200/repositories/_mapping?pretty
```

En plus de cette requête, il faut indiquer le fichier binaire à importer, qui est *github_mapping.json*

Ce qui renvoit:
```json
{
	"acknowledged": true
}
```

Il faut ensuite importer le données avec la methode *_bulk*.
Une fois les données formatées avec le script *csvtojson.py*, la requête suivante, de type **PUT** permet d'importer les données :

*@PUT*
```https
https://localhost:9200/_bulk
```

En plus de la requête, il faut indiquer le fichier binaire *github.json*, qui contient l'ensemble des données.

**Insomnia** insert également dans le header la mention *Content-Type: application/json* qui indique que le contenu est en json.

Ce qui renvoit :
```json
{
	"took": 318,
	"errors": true,
	"items": [
		{
			"index": {
				"_index": "repositories",
				"_type": "_doc",
				"_id": "1",
				"_version": 1,
				"result": "created",
				"_shards": {
					"total": 2,
					"successful": 1,
					"failed": 0
				},
				"_seq_no": 0,
				"_primary_term": 1,
				"status": 201
			}
		},
		...
```

Cela indique que toutes mes données on bien été importer.

Nous pouvons désormais faire des requêtes dans ces données.

Nous allons donc faires des requêtes dans cette collections de données une methode **GET** sur l'url suivante :
```https
https://localhost:9200/repositories/_search?pretty
```

## Requêtes

Pour commencé, disons que nous voulons savoir quels sont, dans ce jeu de données (les valeurs dates de 2017 en générales), les 10 projets les plus étoilées.

La requête suivante renverra les 10 projets les plus étoilées.

*@GET*
```https
https://localhost:9200/repositories/_search?size=10
```

```json
{
	"took": 927,
	"timed_out": false,
	"_shards": {
		"total": 4,
		"successful": 4,
		"skipped": 0,
		"failed": 0
	},
	"hits": {
		"total": {
			"value": 985,
			"relation": "eq"
		},
		"max_score": 1.0,
		"hits": [
			{
				"_index": "repositories",
				"_type": "_doc",
				"_id": "1",
				"_score": 1.0,
				"_source": {
					"Username": "Username",
					"Repository Name": "Repository Name",
					"Description": "Description",
					"Last Update Date": "Last Update Date",
					"Language": "Language",
					"Number of Stars": "Number of Stars",
					"Tags": "Tags",
					"Url": "Url"
				}
			},
			{
				"_index": "repositories",
				"_type": "_doc",
				"_id": "2",
				"_score": 1.0,
				"_source": {
					"Username": "freeCodeCamp",
					"Repository Name": "freeCodeCamp",
					"Description": "The https://freeCodeCamp.com open source codebase and curriculum. Learn to code and help nonprofits.",
					"Last Update Date": "2017-06-24T15:56:17Z",
					"Language": "JavaScript",
					"Number of Stars": "290k",
					"Tags": "nonprofits,certification,curriculum,react,nodejs,javascript,d3,teachers,community,education,programming,math,learn-to-code,careers",
					"Url": "https://github.com/freeCodeCamp/freeCodeCamp"
				}
			},
			{
				"_index": "repositories",
				"_type": "_doc",
				"_id": "3",
				"_score": 1.0,
				"_source": {
					"Username": "twbs",
					"Repository Name": "bootstrap",
					"Description": "The most popular HTML, CSS, and JavaScript framework for developing responsive, mobile first projects on the web.",
					"Last Update Date": "2017-06-24T15:40:21Z",
					"Language": "JavaScript",
					"Number of Stars": "112k",
					"Tags": "javascript,css,html,bootstrap,jekyll-site,scss",
					"Url": "https://github.com/twbs/bootstrap"
				}
			},
			...
		]
	}
}
```

Admettons maintenant que nous voulons les projets les plus étoilées uniquement pour le langage Java.

Je vais donc, par le biais d'une requête **GET** sur l'url de recherche, soumettre la requête par *match* suivante :
```https
https://localhost:9200/repositories/_search?pretty
```
 
```json
{
	"query":{
		"match":{
			"language": "Java"
		}
	}
}
```

Cette requête, au format JSON, nous renvoie:

```json
{
	"took": 5,
	"timed_out": false,
	"_shards": {
		"total": 1,
		"successful": 1,
		"skipped": 0,
		"failed": 0
	},
	"hits": {
		"total": {
			"value": 66,
			"relation": "eq"
		},
		"max_score": 2.6444056,
		"hits": [
			{
				"_index": "repositories",
				"_type": "_doc",
				"_id": "72",
				"_score": 2.6444056,
				"_source": {
					"username": "ReactiveX",
					"repository_name": "RxJava",
					"description": "RxJava  Reactive Extensions for the JVM  a library for composing asynchronous and event-based programs using observ",
					"last_update_date": "2017-06-24T11:34:48Z",
					"language": "Java",
					"number_of_stars": "25.2k",
					"tags": "flow,reactive-streams,java,rxjava",
					"url": "https://github.com/ReactiveX/RxJava"
				}
			},
			{
				"_index": "repositories",
				"_type": "_doc",
				"_id": "84",
				"_score": 2.6444056,
				"_source": {
					"username": "elastic",
					"repository_name": "elasticsearch",
					"description": "Open Source, Distributed, RESTful Search Engine",
					"last_update_date": "2017-06-24T18:33:40Z",
					"language": "Java",
					"number_of_stars": "23.4k",
					"tags": "java,search-engine,elasticsearch",
					"url": "https://github.com/elastic/elasticsearch"
				}
			},
			...
```

Nous avons donc, trié par popularité sur Github en 2017, les projets **uniquement** écrit en Java.

Maintenant, je veux rechercher dans la base les projets contenant le mot *"Linux"*, que ce soit dans le titre du projet ou dans sa description

Je vais donc founir le code json suivant pour formuler la requête.

*@GET*
```https
https://localhost:9200/repositories/_search?pretty
```

```json
{
	"query": {
		"multi_match": {
			"query": "linux",
			"fields":["username", "description"]
		}
	}
}
```

Celle-ci renvoie :

```json
{
	"took": 782,
	"timed_out": false,
	"_shards": {
		"total": 1,
		"successful": 1,
		"skipped": 0,
		"failed": 0
	},
	"hits": {
		"total": {
			"value": 8,
			"relation": "eq"
		},
		"max_score": 6.1539454,
		"hits": [
			{
				"_index": "repositories",
				"_type": "_doc",
				"_id": "18",
				"_score": 6.1539454,
				"_source": {
					"username": "torvalds",
					"repository_name": "linux",
					"description": "Linux kernel source tree",
					"last_update_date": "2017-06-24T09:27:57Z",
					"language": "C",
					"number_of_stars": "46.3k",
					"tags": "",
					"url": "https://github.com/torvalds/linux"
				}
			},
			{
				"_index": "repositories",
				"_type": "_doc",
				"_id": "899",
				"_score": 6.1539454,
				"_source": {
					"username": "boot2docker",
					"repository_name": "boot2docker",
					"description": "Lightweight Linux for Docker",
					"last_update_date": "2017-06-20T22:43:51Z",
					"language": "Shell",
					"number_of_stars": "6.8k",
					"tags": "",
					"url": "https://github.com/boot2docker/boot2docker"
				}
			},
			{
				"_index": "repositories",
				"_type": "_doc",
				"_id": "743",
				"_score": 5.515021,
				"_source": {
					"username": "afaqurk",
					"repository_name": "linux-dash",
					"description": "A beautiful web dashboard for Linux",
					"last_update_date": "2017-05-18T18:32:23Z",
					"language": "JavaScript",
					"number_of_stars": "7.7k",
					"tags": "linux-dash,linux,ui,web,monitoring,dashboard,server",
					"url": "https://github.com/afaqurk/linux-dash"
				}
			},
			...
```

Venant de voir le projet *"Linux"* de **Linus Torvals**, je veux en savoir plus sur ces éventuelles autres projets.

Je vais donc chercher dans la base tout les projets pour le *"username"* torvalds

Je fais donc la requête :

*@GET*
```https
https://localhost:9200/repositories/_search?pretty
```

```json
{
	"query": {
		"match": {
			"username": "torvalds"
		}
	}
}
```

Celle-ci renovie :

```json
{
	"took": 10,
	"timed_out": false,
	"_shards": {
		"total": 1,
		"successful": 1,
		"skipped": 0,
		"failed": 0
	},
	"hits": {
		"total": {
			"value": 1,
			"relation": "eq"
		},
		"max_score": 6.6402693,
		"hits": [
			{
				"_index": "repositories",
				"_type": "_doc",
				"_id": "18",
				"_score": 6.6402693,
				"_source": {
					"username": "torvalds",
					"repository_name": "linux",
					"description": "Linux kernel source tree",
					"last_update_date": "2017-06-24T09:27:57Z",
					"language": "C",
					"number_of_stars": "46.3k",
					"tags": "",
					"url": "https://github.com/torvalds/linux"
				}
			}
		]
	}
}
```

Enfin, je veux maintenant chercher tout les projets concernant les système d'exploitation MacOS et iOS, j'envoie la requête **GET** suivante:


*@GET*
```https:
https://localhost:9200/repositories/_search?pretty
```

```json
{
	"query": {
		"query_string": {
			"query": "MacOS OR Apple"
		}
	}
}
```

Cette requête renvoie :

```json
{
	"took": 12,
	"timed_out": false,
	"_shards": {
		"total": 1,
		"successful": 1,
		"skipped": 0,
		"failed": 0
	},
	"hits": {
		"total": {
			"value": 61,
			"relation": "eq"
		},
		"max_score": 6.7525573,
		"hits": [
			{
				"_index": "repositories",
				"_type": "_doc",
				"_id": "170",
				"_score": 6.7525573,
				"_source": {
					"username": "mathiasbynens",
					"repository_name": "dotfiles",
					"description": " .files, including ~/.macos  sensible hacker defaults for macOS",
					"last_update_date": "2017-06-13T03:27:31Z",
					"language": "Shell",
					"number_of_stars": "16.9k",
					"tags": "macos,dotfiles,bash",
					"url": "https://github.com/mathiasbynens/dotfiles"
				}
			},
			{
				"_index": "repositories",
				"_type": "_doc",
				"_id": "356",
				"_score": 5.515021,
				"_source": {
					"username": "drduh",
					"repository_name": "macOS-Security-and-Privacy-Guide",
					"description": "A practical guide to securing macOS.",
					"last_update_date": "2017-05-23T23:00:23Z",
					"language": "Python",
					"number_of_stars": "11.5k",
					"tags": "disk-encryption,privacy,apple,macos,security,osx,macos-setup",
					"url": "https://github.com/drduh/macOS-Security-and-Privacy-Guide"
				}
			},
			{
				"_index": "repositories",
				"_type": "_doc",
				"_id": "731",
				"_score": 5.515021,
				"_source": {
					"username": "Homebrew",
					"repository_name": "brew",
					"description": " The missing package manager for macOS",
					"last_update_date": "2017-06-24T17:12:01Z",
					"language": "Ruby",
					"number_of_stars": "7.8k",
					"tags": "homebrew,ruby,macos,package-manager,brew",
					"url": "https://github.com/Homebrew/brew"
				}
			},
			...
```

## Aggrégations


**[!]** **Étant donnée que mon dataset n'est que composé de champs texte, il m'est compliqué de faire des aggrégations car nombreuse d'entre elle utilise les nombres, je vais donc faire les requêtes mais ne pas fournir de resultats.**

Je souhaiterais savoir qu'elle est la moyenne d'étoiles de l'ensemble de ces projets. Pour ce faire, je vais envoyer une requête **GET** avec l'aggrégation suivante :

*@GET*
```https:
https://localhost:9200/repositories/_search?pretty
```

```json
{
	"size": 0,
	"aggs": {
		"moyenne":{
			"avg": {
				"field": "number_of_stars"
			}
		}
	}
}
```

Celle-ci devrait renvoyer la moyenne du nombre total d'étoiles.

Je souhaite désormais voir combien de projets comporte chaque language. Je vais donc fournir la requête de type **GET** avec l'aggrégation suivantes :

*@GET*
```https:
https://localhost:9200/repositories/_search?pretty
```

```json
{
	"size": 0,
	"aggs": {
		"nombre_de_projets": {
			"terms": {
				"field": "language.raw"
			}
		}
	}
}
```

Cette aggrétion devrait renvoyer, par language, le nombre de projets total.

Admettons maintenant que nous souhaitons voir qu'elle est, en pourcentage, le language le plus utilisé sur l'ensemble des projets.

*@GET*
```https:
https://localhost:9200/repositories/_search?pretty
```

```json
{
	"size": 0,
	"aggs": {
		"pourcentage_language": {
			"percentiles": {
				"field": "language"
			}
		}
	}
}
```

Cette requête devrait renvoyer, pour chaque language, un pourcentage représentant le nombre de projets utilisant le language en question.

Enfin, je veux désormais en savoir plus sur le nombres d'étoiles pour cet ensemble de projets et veux donc afficher quelques statistiques.

*@GET*
```https:
https://localhost:9200/repositories/_search?pretty
```

```json
{
	"size": 0,
	"aggs": {
		"stats_etoiles": {
			"stats": {
				"field": "number_of_stars"
			}
		}
	}
}
```

cette requête devrait me renvoyer des informations "count", "min", "max", "avg" & "sum.

**[!]** **À noter que ce dataset ne contient que des champs textes, et que les données qui auraient pus être numérique ne sont pas exploitable correctement, comment par exemple le nombre d'étoiles qui est au format *"100k"*, qui ne peut être autre chose qu'un texte. Il m'a donc été difficile de trouvé des requête pertinante à effectuer.**