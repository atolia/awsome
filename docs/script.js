document.addEventListener('DOMContentLoaded', run);

function run() {
  defItem = menu.children[0].id

  link = (location.hash || '#' + defItem).replace('#','')
  el = document.getElementById(link)
  el.style.background = 'black';
  // link_latest.style.background = 'black';
  show(el)
}

function show(arg) { 
  Array.from(arg.parentNode.children).forEach(
    element => {
      el=element.id.trim().split('_')[1]
      // console.log(el)
      if(el!="") {
        document.getElementById(el).style.display="none"
        document.getElementById('link_'+el).style.background = 'darkgray'
      }
    }
  )
  document.getElementById(arg.id).style.background = 'black'
  document.getElementById(arg.id.split('_')[1]).style.display="block" 
}
