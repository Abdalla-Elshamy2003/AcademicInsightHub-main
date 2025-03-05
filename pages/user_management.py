import streamlit as st
from database import get_db
from models import User, Role, UserRole
from utils import show_success, show_error, show_warning, show_info, rerun, paginate_data
from datetime import datetime
import json

st.title("User Management")

# Check if user is admin
if "user" not in st.session_state or st.session_state.user.get("role") != "admin":
    show_error("You do not have permission to access this page.")
    st.stop()

# Tabs for different user management functions
tabs = st.tabs(["User List", "Create User", "Manage Roles"])

# --- Tab 1: User List ---
with tabs[0]:
    st.header("User List")
    
    # Get all users
    db = next(get_db())
    users = db.query(User).all()
    
    # Search functionality
    search_term = st.text_input("Search users by username or email", key="user_search")
    if search_term:
        users = [user for user in users if search_term.lower() in user.username.lower() or 
                (user.email and search_term.lower() in user.email.lower())]
    
    # Paginate users
    paginated_users = paginate_data(users, items_per_page=10, key="users_management")
    
    # Display users in a table
    user_data = []
    for user in paginated_users:
        # Get user role
        user_role = db.query(UserRole).filter_by(user_id=user.id).first()
        role_name = db.query(Role).get(user_role.role_id).name if user_role else "No role"
        
        # Format last login
        last_login = user.last_login.strftime("%Y-%m-%d %H:%M") if user.last_login else "Never"
        
        user_data.append({
            "ID": user.id,
            "Username": user.username,
            "Email": user.email,
            "Role": role_name,
            "Created": user.created_at.strftime("%Y-%m-%d"),
            "Last Login": last_login
        })
    
    # Display as dataframe
    st.dataframe(user_data)
    
    # User details and actions
    selected_user_id = st.selectbox("Select user to manage", 
                                  options=[user.id for user in paginated_users],
                                  format_func=lambda x: next((u.username for u in paginated_users if u.id == x), ""))
    
    if selected_user_id:
        selected_user = next((u for u in paginated_users if u.id == selected_user_id), None)
        if selected_user:
            with st.expander(f"Manage User: {selected_user.username}", expanded=True):
                # User details
                st.write(f"**Username:** {selected_user.username}")
                st.write(f"**Email:** {selected_user.email}")
                st.write(f"**Created:** {selected_user.created_at.strftime('%Y-%m-%d %H:%M')}")
                st.write(f"**Last Login:** {last_login}")
                
                # Change role
                user_role = db.query(UserRole).filter_by(user_id=selected_user.id).first()
                current_role_id = user_role.role_id if user_role else None
                
                roles = db.query(Role).all()
                role_options = [(role.id, role.name) for role in roles]
                
                col1, col2 = st.columns(2)
                with col1:
                    new_role_id = st.selectbox(
                        "Change Role",
                        options=role_options,
                        format_func=lambda x: x[1],
                        index=next((i for i, r in enumerate(role_options) if r[0] == current_role_id), 0)
                    )
                    
                    if st.button("Update Role"):
                        if new_role_id[0] != current_role_id:
                            try:
                                if user_role:
                                    user_role.role_id = new_role_id[0]
                                else:
                                    user_role = UserRole(
                                        user_id=selected_user.id,
                                        role_id=new_role_id[0],
                                        created_at=datetime.utcnow()
                                    )
                                    db.add(user_role)
                                
                                db.commit()
                                show_success(f"Role updated for {selected_user.username}")
                            except Exception as e:
                                db.rollback()
                                show_error(f"Error updating role: {str(e)}")
                
                with col2:
                    # Reset password
                    if st.button("Reset Password"):
                        st.session_state["resetting_password_for"] = selected_user.id
                        rerun()
                    
                    # Delete user
                    delete_key = f"delete_user_{selected_user.id}"
                    if delete_key not in st.session_state:
                        st.session_state[delete_key] = False
                    
                    if st.button("Delete User"):
                        st.session_state[delete_key] = True
                    
                    if st.session_state[delete_key]:
                        st.warning(f"Are you sure you want to delete user '{selected_user.username}'? This action cannot be undone.")
                        confirm_col1, confirm_col2 = st.columns(2)
                        with confirm_col1:
                            if st.button("Yes, Delete", key=f"confirm_delete_user_{selected_user.id}"):
                                try:
                                    db.delete(selected_user)
                                    db.commit()
                                    show_success(f"User '{selected_user.username}' deleted successfully.")
                                    st.session_state[delete_key] = False
                                    rerun()
                                except Exception as e:
                                    db.rollback()
                                    show_error(f"Error deleting user: {str(e)}")
                        with confirm_col2:
                            if st.button("Cancel", key=f"cancel_delete_user_{selected_user.id}"):
                                st.session_state[delete_key] = False
                                rerun()
        
        # Password reset form
        if "resetting_password_for" in st.session_state:
            reset_user = db.query(User).get(st.session_state["resetting_password_for"])
            if reset_user:
                st.subheader(f"Reset Password for {reset_user.username}")
                
                with st.form("reset_password_form"):
                    new_password = st.text_input("New Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")
                    submit = st.form_submit_button("Reset Password")
                
                if submit:
                    if new_password and new_password == confirm_password:
                        try:
                            from utils import hash_password
                            hashed_password, salt = hash_password(new_password)
                            
                            reset_user.password = hashed_password
                            reset_user.salt = salt
                            reset_user.updated_at = datetime.utcnow()
                            
                            db.commit()
                            show_success("Password reset successfully")
                            st.session_state.pop("resetting_password_for")
                            rerun()
                        except Exception as e:
                            db.rollback()
                            show_error(f"Error resetting password: {str(e)}")
                    else:
                        show_error("Passwords do not match or are empty")
                
                if st.button("Cancel Reset"):
                    st.session_state.pop("resetting_password_for")
                    rerun()
    else:
        st.info("No users found.")

# --- Tab 2: Create User ---
with tabs[1]:
    st.header("Create New User")
    
    with st.form("create_user_form"):
        username = st.text_input("Username (3-50 characters, alphanumeric)")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password", 
                               help="At least 8 characters with uppercase, lowercase, number, and special character")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        # Get roles for dropdown
        db = next(get_db())
        roles = db.query(Role).all()
        role_options = [(role.id, role.name) for role in roles]
        
        role_choice = st.selectbox(
            "Role",
            options=role_options,
            format_func=lambda x: x[1]
        )
        
        submit = st.form_submit_button("Create User")
    
    if submit:
        # Validate inputs
        from utils import validate_username, validate_email, validate_password_strength
        
        valid_inputs = True
        
        if not username or not email or not password or not confirm_password:
            show_error("Please fill in all fields")
            valid_inputs = False
        
        if valid_inputs and not validate_username(username):
            show_error("Username must be 3-50 characters and contain only letters, numbers, and underscores")
            valid_inputs = False
            
        if valid_inputs and not validate_email(email):
            show_error("Please enter a valid email address")
            valid_inputs = False
            
        if valid_inputs:
            is_strong, message = validate_password_strength(password)
            if not is_strong:
                show_error(message)
                valid_inputs = False
                
        if valid_inputs and password != confirm_password:
            show_error("Passwords do not match")
            valid_inputs = False
            
        if valid_inputs:
            # Check if username or email already exists
            existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                show_error("Username or email already exists")
                valid_inputs = False
        
        if valid_inputs:
            try:
                from utils import hash_password
                hashed_password, salt = hash_password(password)
                
                # Create new user
                new_user = User(
                    username=username,
                    email=email,
                    password=hashed_password,
                    salt=salt,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                db.add(new_user)
                db.flush()  # Get the user ID
                
                # Assign role
                user_role = UserRole(
                    user_id=new_user.id,
                    role_id=role_choice[0],
                    created_at=datetime.utcnow()
                )
                
                db.add(user_role)
                db.commit()
                
                show_success(f"User '{username}' created successfully")
            except Exception as e:
                db.rollback()
                show_error(f"Error creating user: {str(e)}")

# --- Tab 3: Manage Roles ---
with tabs[2]:
    st.header("Manage Roles")
    
    # Get all roles
    db = next(get_db())
    roles = db.query(Role).all()
    
    # Display roles
    for role in roles:
        with st.expander(f"Role: {role.name.capitalize()}", expanded=False):
            # Display permissions
            st.write("**Permissions:**")
            permissions = json.loads(role.permissions)
            
            # Group permissions by category
            categories = {
                "Content": [p for p in permissions.keys() if any(x in p for x in ["course", "chapter", "question"])],
                "Analytics": [p for p in permissions.keys() if any(x in p for x in ["analytics", "feedback", "progress"])],
                "System": [p for p in permissions.keys() if any(x in p for x in ["user", "role", "system", "export", "import"])]
            }
            
            for category, perms in categories.items():
                if perms:
                    st.write(f"*{category}:*")
                    for perm in perms:
                        st.write(f"- {perm.replace('_', ' ').capitalize()}: {'✅' if permissions[perm] else '❌'}")
            
            # Count users with this role
            user_count = db.query(UserRole).filter_by(role_id=role.id).count()
            st.write(f"**Users with this role:** {user_count}")
            
            # Edit role permissions (for custom roles only)
            if role.name not in ["admin", "professor", "student", "teaching_assistant"]:
                if st.button(f"Edit {role.name} Permissions", key=f"edit_role_{role.id}"):
                    st.session_state["editing_role"] = role.id
                    rerun()
    
    # Create new role
    st.subheader("Create New Role")
    
    with st.form("create_role_form"):
        role_name = st.text_input("Role Name")
        
        # Permission categories
        st.write("**Content Permissions:**")
        create_course = st.checkbox("Create Course")
        edit_course = st.checkbox("Edit Course")
        delete_course = st.checkbox("Delete Course")
        create_chapter = st.checkbox("Create Chapter")
        edit_chapter = st.checkbox("Edit Chapter")
        delete_chapter = st.checkbox("Delete Chapter")
        create_question = st.checkbox("Create Question")
        edit_question = st.checkbox("Edit Question")
        delete_question = st.checkbox("Delete Question")
        
        st.write("**Analytics Permissions:**")
        view_analytics = st.checkbox("View Analytics")
        view_feedback = st.checkbox("View Feedback")
        submit_feedback = st.checkbox("Submit Feedback")
        
        st.write("**System Permissions:**")
        export_data = st.checkbox("Export Data")
        import_data = st.checkbox("Import Data")
        
        submit = st.form_submit_button("Create Role")
    
    if submit and role_name:
        # Check if role name already exists
        existing_role = db.query(Role).filter_by(name=role_name.lower()).first()
        if existing_role:
            show_error(f"Role '{role_name}' already exists")
        else:
            # Create permissions dictionary
            permissions = {
                "create_course": create_course,
                "edit_course": edit_course,
                "delete_course": delete_course,
                "create_chapter": create_chapter,
                "edit_chapter": edit_chapter,
                "delete_chapter": delete_chapter,
                "create_question": create_question,
                "edit_question": edit_question,
                "delete_question": delete_question,
                "view_analytics": view_analytics,
                "view_feedback": view_feedback,
                "submit_feedback": submit_feedback,
                "export_data": export_data,
                "import_data": import_data
            }
            
            try:
                # Create new role
                new_role = Role(
                    name=role_name.lower(),
                    permissions=json.dumps(permissions),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                db.add(new_role)
                db.commit()
                
                show_success(f"Role '{role_name}' created successfully")
                rerun()
            except Exception as e:
                db.rollback()
                show_error(f"Error creating role: {str(e)}") 