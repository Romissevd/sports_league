let groups = document.querySelectorAll("[id*=\"group \"]");

function buttonClick (group){
    let groupClick = `group ${group.value}`;
    for (i = 0; i < groups.length; i++) {
        let groupInList = groups[i];
        if (groupInList.id == groupClick) {
            groupInList.className = 'showed';
        } else {
            groupInList.className = '';
        }
    }
}
