# <a href="http://viniciushedler.github.io/hackathon-1sti">Libr.as 👋</a> - *Hackathon 1sti*
![Logo Libr.as](images/logo.png) <br>

Libr.as é um jogo de adivinhação de palavras onde você digita fazendo sinais em Libras, desenvolvido para o [1º Hackathon 1sti](https://1sti.com.br/) - FGV. <br>
Acesse o jogo por [aqui](http://viniciushedler.github.io/hackathon-1sti) ou leia mais a respeito abaixo.

*GRUPO:* ***KNN - K Nearest Nerds*** <br>
***Membros:*** *Lf Laguardia, Bruno Fornaro, Vinicius Hedler, Marcelo Amaral, Gianlucca Devigili*

## Problema: Difusão do Aprendizado de Libras

A Linguagem Brasileira de Sinais ([LIBRAS](http://www.pessoacomdeficiencia.curitiba.pr.gov.br/conteudo/libras/127#:~:text=A%20L%C3%ADngua%20Brasileira%20de%20Sinais,24%20de%20abril%20de%202002.)) é reconhecida por lei como a segunda língua oficial do Brasil, sendo um meio de comunicação importante para pessoas com deficiência auditiva. Nesse mesmo contexto, no [censo de 2010](https://blog.signumweb.com.br/curiosidades/quantos-surdos-falam-libras-no-brasil/) foi estimado que cerca de 5% da população brasileira  apresenta algum nível de deficiência auditiva. Assim, entendemos que é importante que o maior número de pessoas possível (idealmente todas) saibam se comunicar utilizando LIBRAS, para evitarmos problemas de inclusão com as pessoas que possuem deficiência auditiva na sociedade.

Embora não tenha sido estimado o número de pessoas fluentes (ou que consigam se comunicar minimamente) em LIBRAS no censo de 2010, entendemos que quando se trata de aprendizado, no geral, o interesse é um fator importante para que alguém aprenda algo novo. Nesse sentido, vemos que o aprendizado de LIBRAS pode ainda ser pouco difundido e incentivado no país e desejamos focar nesse problema sob o aspecto de aumentar o interesse do maior número de pessoas possível em aprender LIBRAS.

## Solução: Tornar o Aprendizado mais Interessante
Tendo em vista o problema apresentado, desejamos instigar as pessoas a aprender LIBRAS, na esperança de aumentar o número de pessoas na população que saiba LIBRAS e consiga utilizar essa língua suficientemente para se expressar e conseguir comunicar outros fluentes por meio dela.

Dessa forma, a base da nossa solução foi desenvolver uma forma _gamificada_ de aprender LIBRAS. Propomos esta solução com a intenção de aumentar o interesse dos usuários em aprender LIBRAS, mesmo que possa ser indiretamente. Isto é, com isso, o usuário pode estar apenas com a intenção de jogar em nossa plataforma (pois também nos preocupamos no aspecto de deixar o jogo atrativo), mas também irá aprender LIBRAS enquanto joga e se diverte.

Inicialmente, temos implementado um jogo no qual o usuário deve tentar adivinhar uma palavra submetendo tentativas de acertar a palavras (inteira), semelhante a como funciona o jogo [term.ooo](https://term.ooo/). No caso, para que o jogador consiga escrever as letras da palavra, ele deve fazer os sinais do alfabeto em LIBRAS para que a câmera do dispositivo que ele estiver utilizando capture a imagem dele fazendo o sinal (no qual será processado pela ferramenta que implementamos) e a letra seja reconhecida e escrita na tela.

## Descrição: Viabilidade de uso e aplicações
Da maneira que propomos nossa ferramenta, conseguimos hospedá-la em um [site](https://viniciushedler.github.io/hackathon-1sti/) e, assim, fazemos com que ela seja acessível de forma simples, o usuário apenas precisa ter aceso a um computador que possua uma webcam e acesso à internet.

Com isso, temos a possibilidade de atingir milhares de pessoas, e podemos ver como base alguns dos jogos que nos inspiraram como o [wordle](https://www.nytimes.com/games/wordle/index.html) e o [term.ooo](https://term.ooo/), que chegaram a receber [2 milhões](https://g1.globo.com/pop-arte/games/noticia/2022/01/19/wordle-e-termo-historia-de-amor-se-transformou-em-jogo-de-palavras-que-e-sensacao-em-2022.ghtml) de acessos diários e [400 mil](https://super.abril.com.br/tecnologia/termo-batemos-um-papo-com-o-criador-da-versao-em-portugues-do-jogo-wordle/) acessos diários, respectivamente.