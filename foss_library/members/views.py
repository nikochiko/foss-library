from math import ceil

from flask import Blueprint, flash, request, redirect, render_template

from foss_library.decorators import get_model_instance_from_id
from foss_library.utils import flash_form_errors
from .forms import CreateMemberForm, UpdateMemberForm
from .models import Member

blueprint = Blueprint(
    "members", __name__, url_prefix="/members", static_folder="../static"
)


@blueprint.route("/", methods=("GET",))
def list_members():
    """List members"""
    members_on_each_page = 20

    total_pages = max(ceil(Member.query.count() / members_on_each_page), 1)

    # get page from request args, e.g. /books?page=1
    page = request.args.get("page", 1)
    page = int(page)

    if page > 1 and page > total_pages:
        flash(f"Page {page} is out of range", "warning")

    # set limit and offset for SQL query
    limit = members_on_each_page
    offset = (page - 1) * members_on_each_page

    members = (
        Member.query.limit(limit).offset(offset).all()
    )
    return render_template(
        "members/list_members.html",
        members=members,
        current_page=page,
        total_pages=total_pages,
    )


@blueprint.route("/create/", methods=("GET", "POST"))
def create_member():
    """Create a new member"""
    form = CreateMemberForm()
    if form.validate_on_submit():
        member = Member()
        form.populate_obj(member)
        member.save()
        flash("Member added successfully!", "success")
        return redirect("/members/")

    flash_form_errors(form)
    if form.errors:
        status_code = 400
    else:
        status_code = 200

    return render_template("members/create_member.html", form=form), status_code


@blueprint.route("/update/<int:id>", methods=("GET", "POST"))
@get_model_instance_from_id(Member)
def update_member(member):
    """Update an existing member"""
    form = UpdateMemberForm(obj=member)
    if form.validate_on_submit():
        form.populate_obj(member)
        member.save()
        flash("Member updated successfully!", "success")
        return redirect("/members/")

    flash_form_errors(form)
    if form.errors:
        status_code = 400
    else:
        status_code = 200

    return render_template("members/update_member.html", form=form), status_code


@blueprint.route("/delete/<int:id>", methods=("POST",))
@get_model_instance_from_id(Member)
def delete_member(member):
    """Delete a member"""
    member.delete()
    flash("Member deleted successfully!", "success")
    return redirect("/members/")
