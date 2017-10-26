## dip株式会社

## 実行方法
terminalで`/motemote` に移動して
```
python manage.py runserver --setting='motemote.settings.development'
```
を実行

## デプロイ方法
[Django&Nginx&uWSGIでのデプロイの参考文献](http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html)

ここでは、すでにサーバにssh接続でアクセスしていると想定。これから、`AWSサーバ × Nginx × uwsgi`でのデプロイ方法を示す。

```
$ sudo -s
$ vi /etc/nginx/conf.d/motemote.conf
```
serverを明記するor明記されていることを確認する。以下nginxの設定ファイル

`motemote.conf`
```
upstream django {
    server unix:///var/www/motemote_project/motemote/mysite.sock;
}

server {
    listen      80;
    server_name motemote.ai;
    charset     utf-8;

    client_max_body_size 75M;

    location /static {
        alias /var/www/motemote_project/motemote/static;
    }

    location / {
        uwsgi_pass  django;
        include     /var/www/motemote_project/motemote/uwsgi_params;
    }
}
```

```
$ /etc/init.d/nginx restart
$ uwsgi --emperor /etc/uwsgi/vassals --uid user --gid user --logto /var/log/uwsgi/motemote.log
```
以上！

### member
`satotatsu matchan zukako nabetaro tamutamu`
