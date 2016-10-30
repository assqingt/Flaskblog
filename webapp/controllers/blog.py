#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import path
import datetime
from flask import Flask, render_template, redirect, request, url_for, g, session, abort, Blueprint
from sqlalchemy import func, desc

from webapp.models import db,Post,Tag,Comment,User,tags
from webapp.forms import CommentForm, PostForm

from flask_login import login_required,current_user

#bolg蓝图
blog_blueprint = Blueprint(
	'blog',
	__name__,
	template_folder='../templates/blog',
	url_prefix='/blog'
)


# @blog_blueprint.before_request
# def check_user():
# 	if 'username' in session:
# 		g.current_user = User.query.filter_by(username=session['username']).one()
# 	else:
# 		g.current_user = None



# 取最新文章和最常用tag
def sidebar_data():
	recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
	top_tags = db.session.query(Tag, func.count(tags.c.post_id).label('total')).join(tags).group_by(Tag).order_by(
		desc('total')).limit(5).all()

	return recent, top_tags
#views######################################################

@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
	posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, 10)
	recent, top_tags = sidebar_data()

	return render_template('blog/home.html', posts=posts, recent=recent, top_tags=top_tags)


@blog_blueprint.route('/post/<int:post_id>', methods=('GET', 'POST'))
def post(post_id):
	form = CommentForm()
	if form.validate_on_submit():
		new_comment = Comment()
		new_comment.name = form.name.data
		new_comment.text = form.text.data
		new_comment.post_id = post_id
		new_comment.date = datetime.datetime.now()
		db.session.add(new_comment)
		db.session.commit()
		form.name.data = None
		form.text.data = None
	post = Post.query.get_or_404(post_id)
	tags = post.tags
	comments = post.comments.order_by(Comment.date.desc()).all()
	recent, top_tags = sidebar_data()

	if request.method == 'POST':
		return redirect(url_for('blog.post', post_id=post_id))
	else:
		return render_template('blog/post.html', post=post, tags=tags, comments=comments, recent=recent, top_tags=top_tags,
		                       form=form)


@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
	tag = Tag.query.filter_by(title=tag_name).first_or_404()
	posts = tag.posts.order_by(Post.publish_date.desc()).all()
	recent, top_tags = sidebar_data()

	return render_template('blog/tag.html', tag=tag, posts=posts, recent=recent, top_tags=top_tags)


@blog_blueprint.route('/user/<string:username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = user.posts.order_by(Post.publish_date.desc()).all()
	recent, top_tags = sidebar_data()

	return render_template('blog/user.html', user=user, posts=posts, recent=recent, top_tags=top_tags)

@blog_blueprint.route('/new',methods=['GET','POST'])
@login_required
def new_post():
	# if not g.current_user:
	# 	return redirect(url_for('main.login'))

	form = PostForm()

	if form.validate_on_submit():
		new_post = Post(form.title.data)
		new_post.text = form.text.data
		new_post.publish_date = datetime.datetime.now()
		# new_post.user = g.current_user
		new_post.user = current_user


		db.session.add(new_post)
		db.session.commit()


	return render_template('blog/new.html',form=form)


@blog_blueprint.route('/edit/<int:id>',methods=['GET','POST'])
def edit_post(id):
	if not current_user:
		return redirect(url_for('main.login'))

	post = Post.query.get_or_404(id)

	if current_user != post.user:
		abort(403)

	form = PostForm()

	if form.validate_on_submit():
		post.title = form.title.data
		post.text = form.text.data
		post.publish_date = datetime.datetime.now()

		db.session.add(post)
		db.session.commit()

		return redirect(url_for('.post',post_id=post.id))

	form.text.data = post.text

	return render_template('edit.html',form=form,post=post)



































# @blog_blueprint.before_request
# def before_request():
# 	if 'user_id' in session:
# 		g.user = User.query.get(session['user_id'])
# 	else:
# 		g.user = None
#
#
# @blog_blueprint.route('/restricted')
# def admin():
# 	if g.user is None:
# 		abort(403)
# 	return render_template('blog/admin.html')
#
# @blog_blueprint.errorhandler(404)
# def page_not_found(error):
# 	return render_template('blog/page_not_found.html'), 404
