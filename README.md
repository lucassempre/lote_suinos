Este teste teve como objetivo criar uma aplicação que execute ações de CRUD de forma assíncrona. As mensagens são enfileiradas pelo RabbitMQ e consumidas pelos workers do Celery.

A arquitetura hexagonal foi adotada para manter o teste mais legível e modular.

### 1. Core (Núcleo) (Use Case)
- **core/domain/models.py:** Define o modelo de dados do lote de forma independente do armazenamento.
- **core/domain/repositories.py:** Define a interface para repositórios que gerenciam os lotes, abstraindo as operações de armazenamento.
- **core/application/lote.py:** Implementa a lógica de negócios proposta como CRUD.
- **core/application/task.py:** Implementa o consumo assíncrono das mensagens pelo Celery.

### 2. Infrastructure (Infraestrutura) (Adapters)
- **core/infrastructure/models.py:** Implementa a persistência dos dados utilizando o Django ORM para manipulação dos lotes.
- **core/infrastructure/repositories.py:** Implementa o repositório concreto `LoteRepository`, interagindo com `LoteModel` para acessar e manipular os dados.
- **core/infrastructure/serializers.py:** Implementa a serialização dos dados. Esta implementação está totalmente acoplada ao Django Rest Framework (DRF).

### 3. Interfaces (Ports)
- **core/interfaces/views.py:** Define as views do DRF, habilitando as funcionalidades do CRUD.
- **core/interfaces/urls.py:** Define as rotas da aplicação.

## Como Executar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/lucassempre/lote_suinos
   ```
   
2. Edite o env.template de acordo com suas necessidades e renomeie-o para .env:
    ```bash
    cp env.template .env
    ```

3. Execute o Docker:
    ```bash
    docker compose up
    ```

4. Aguarde a inicialização. Sua aplicação estará pronta para uso. Caso queira realizar os testes, execute o seguinte comando após a aplicação estar funcionando:
    ````bash
    docker exec -it app python3 manage.py test -v 2
    ````

A aplicação também se encontra em execução no seguinte link:
```
http://142.93.195.166/api/lotes/
```
Sua documentação interativa:
```
http://142.93.195.166/swagger/
http://142.93.195.166/redoc/
```
