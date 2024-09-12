document.addEventListener('DOMContentLoaded', function() {
    const newHashtagsInput = document.getElementById('id_new_hashtags');
    const existingHashtagsSelect = document.getElementById('id_hashtags');

    newHashtagsInput.addEventListener('blur', function() {
        const newHashtags = newHashtagsInput.value.split(',').map(tag => tag.trim()).filter(tag => tag !== "");
        newHashtags.forEach(tag => {
            const option = document.createElement('option');
            option.text = tag;
            option.value = tag;
            option.selected = true; 
            existingHashtagsSelect.add(option);
        });
    });
});
