# WikiBot (Version 2.1)

## General

### Presentation

WikiBot is a discord bot which makes wikipedia research, weather forecasts and more…

The last version was released on the 23 of May 2021.

### License

This code was provided with license GNU General Public License v3.0.

### Adding WikiBot

For adding WikiBot to your server, please [click here](https://discord.com/api/oauth2/authorize?client_id=731043686682591263&permissions=277025508352&scope=bot).

## Features and command

### Get a list of random articles from wikipedia

`/r number_of_random_article [; language]`

### Get the summary of an article from wikipedia

`/p name_of_article [; language]`

`/p+ name_of_the_article [; language]`
This last function apply an automatic correction on the title given.

### Make a research on wikipedia

`/s search_terms [; language]`

### Get the last news

`/n the_newspaper's_name [; number_of_newspaper_articles [+]]`

### Get the weather

The weather forecasts are provided by the OpenWeather's API.

`/w the_city_name [; day_of_the_forecast]`

The day parameter allow you to see the day. 0 is today, 1 tomorrow… The maximum is 7.


## language parameter

This argument allows you to choose the language of article on wikipedia or the destination language for translations. This parameter is optional, per default language is set on english. For change this, please use ISO abbreviations.

## Exemple

### Wikipedia handlings

`/r 1 ; de` 
Returns a random article in german.

`/p Paris ; fr`
Returns the Paris's wikipedia page in french.

If you have a doubt on the spelling of your search, use `/p+ …`.

`/s Sea`
Returns a list of wikipedia pages in english about the 'sea'.

### The newspaper

`/n The Lancet`
Returns the last article of the Lancet.

`/n The Lancet ; 2`
Returns the two last articles of The Lancet.

`/n The Lancet ; 2+`
Returns the second article only.

The number of the article is specified on the embed title.


### The weather

`/w Paris ; 1`
Returns the weather for Paris tomorrow.
