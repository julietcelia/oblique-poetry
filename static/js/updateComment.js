editButtons = document.querySelectorAll('.edit-poem-comment');

for (const button of editButtons) {
  button.addEventListener('click', () => {
    const newComment = prompt('What would you like your new comment to be?');
    const formInputs = {
      updated_comment: newComment,
      comment_id: button.id,
    };

    fetch('/update_comment', {
      method: 'POST',
      body: JSON.stringify(formInputs),
      headers: {
        'Content-Type': 'application/json',
      },
    }).then((response) => {
      if (response.ok) {
        document.querySelector(`div.comment_num_${button.id}`).innerHTML = newComment;
      } else {
        alert('Failed to update comment.');
      }
    });
  });
}