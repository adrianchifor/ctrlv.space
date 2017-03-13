# [Ctrl + V Space](https://ctrlv.space)

Encrypted paste service. **Encryption only happens on the client-side** and the **password never reaches the server**.

Uses Redis for storing encrypted content.

URL structure:

https://ctrlv.space/*key*#*password*

where:

- *key*: used to retrieve the encypted content from the server.
- *password*: used to decrypt the content. **This is never sent to the server** as it resides after the # fragment.

## Env vars
```
REDIS_URL (if using dokku, will be automatically set when linking with Redis service)
```

## Run

Using [dokku](http://dokku.viewdocs.io/dokku/):
* Create `ctrlv` app on dokku
* Create a Redis service on dokku using this [plugin](https://github.com/dokku/dokku-redis) and link it with `ctrlv` (this will set the `REDIS_URL` env var)
* Set the dokku remote in the git repo:
`git remote add dokku dokku@example.com:ctrlv`
* Deploy:
`git push dokku master`

### License

Copyright &copy; 2017 Adrian Chifor

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
