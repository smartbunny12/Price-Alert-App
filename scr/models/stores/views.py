import json

from flask import Blueprint, render_template, request, redirect, url_for

from scr.models.stores.store import Store

store_buleprint =Blueprint('stores', __name__)

@store_buleprint.route('/')
def index():
    stores=Store.all()
    return render_template('stores/store_index.html', stores=stores)

@store_buleprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('stores/store.html', store=Store.get_by_id(store_id))


@store_buleprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
def edit_store(sotre_id):
    if request.method =='POST':
        pass
    return

@store_buleprint.route('/delete/<string:store_id>')
def delete_store():
    return


@store_buleprint.route('/new', methods=['GET', 'POST'])
def create_store():
    if request.method=='POST':
        name=request.form['name']
        url_prefix=request.form['url_prefix']
        tag_name=request.form['tag_name']
        query=json.loads(request.form['query'])

        Store(name, url_prefix, tag_name, query).save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('stores/new_store.html')

