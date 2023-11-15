document.addEventListener('DOMContentLoaded', () => {
  edit_post();
  submit_changes();
  like_post();
});

function edit_post() {
  const editButtons = document.querySelectorAll('.edit-button');

  editButtons.forEach(button => {
    button.addEventListener('click', () => {
      const postId = button.getAttribute('data-post-id');
      const post = document.querySelector(`div[id="${postId}"]`)
      const postContent = post.querySelector('.post-content');
      const editForm = post.querySelector('.edit-form');
      const newContentField = post.querySelector('.new-content');

      if (editForm.style.display === 'block') {
        editForm.style.display = 'none';
        button.textContent = 'Edit';
      } else {
        editForm.style.display = 'block';
        newContentField.value = postContent.textContent;
        button.textContent = 'Cancel';
      }
    });
  });
}

function submit_changes() {
  const saveButtons = document.querySelectorAll('.save-button');

  saveButtons.forEach(button => {
    button.addEventListener('click', () => {
      const postId = button.getAttribute('data-post-id');
      const post = document.querySelector(`div[id="${postId}"]`)
      newContent = post.querySelector('.new-content').value

      fetch(`/edit/${postId}`, {
        method: 'PUT',
        headers: {
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
          body: newContent
        }),
      })
        .then(response => {
          if (response.ok) {
            const postContent = post.querySelector('.post-content');
            postContent.textContent = newContent;
            const editForm = post.querySelector('.edit-form');
            const editButton = post.querySelector('.edit-button');
            editForm.style.display = 'none';
            editButton.textContent = 'Edit';
          }
          return response.json()
        })
        .then(result => {
          console.log(result);
        })
        .catch(error => {
          console.error('Error:', error);
        });
    });
  });
}

function like_post() {
  const likeButtons = document.querySelectorAll('.like-button');

  likeButtons.forEach(button => {
    button.addEventListener('click', () => {
      const postId = button.getAttribute('data-post-id');
      const post = document.querySelector(`div[id="${postId}"]`);
      const likeCountElement = post.querySelector('.like-count');
      const isLiked = button.textContent.includes("Like");

      fetch(`/like/${postId}`, {
        method: "POST",
        headers: {
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
          liked: isLiked
        }),
      })
        .then(response => response.json())
        .then(data => {
          console.log(data.message);
          button.textContent = data.like_button_text;
          likeCountElement.textContent = data.likes_count;
        })
        .catch(error => {
          console.error('Error:', error);
        });
    });
  });
}