
function IsNumeric(input){
	return (input - 0) == input && input.length > 0;
}


function NumberInRange(x,a,b){
	if(!IsNumeric(x)){return false;}
	else{ return (x>=a && x<=b);}
}

function loadSearchRead(){
	if ($('#length_sign').val()==4){
		$('#divBetweenLength').show();
		$('#divBetweenLength').css('display','inline');
		$('#length').hide();
	}
	if ($('#length_sign').val()>0 && $('#length_sign').val()!=4){$('#length').show();$('#divBetweenLength').hide();}
	if ($('#gc_sign').val()==4){
		$('#divBetweenGC').show();
		$('#divBetweenGC').css('display','inline');
		$('#gc').hide();
	}
	if ($('#gc_sign').val()>0 && $('#gc_sign').val()!=4){$('#gc').show();$('#divBetweenGC').hide();}
}

function searchReads(){
	flag=true;
	len=$('#length').val();
	if($('#length_sign').val()!=4 && !NumberInRange(len,0,1200)){ $('#val_length').show(250); flag=false;} 
	if ($('#length_sign').val()==4){
		len1=$('#length1').val(); len2=$('#length2').val();
		if(!NumberInRange(len1,0,1200) || !NumberInRange(len2,0,1200)){ $('#val_length').show(250); flag=false;	}
	}
	pgc=$('#gc').val();
	if($('#gc_sign').val()!=4 && !NumberInRange(pgc,0,100)){ $('#val_gc').show(250); flag=false;} 
	if ($('#gc_sign').val()==4){
	pgc1=$('#gc1').val(); pgc2=$('#gc2').val();
		if(!NumberInRange(pgc1,0,100) || !NumberInRange(pgc2,0,100)){$('#val_gc').show(250); flag=false;}
	}
	if(flag){$('#formRead').submit();} else {return false;}
}

function loadSearchContig(){
	if ($('#length_sign').val()==4){
		$('#divBetweenLength').show();
		$('#divBetweenLength').css('display','inline');
		$('#length').hide();
	}
	if ($('#length_sign').val()>0 && $('#length_sign').val()!=4){$('#length').show();$('#divBetweenLength').hide();}
	if ($('#gc_sign').val()==4){
		$('#divBetweenGC').show();
		$('#divBetweenGC').css('display','inline');
		$('#gc').hide();
	}
	if ($('#gc_sign').val()>0 && $('#gc_sign').val()!=4){$('#gc').show();$('#divBetweenGC').hide();}
	if ($('#nreads_sign').val()==4){
		$('#divBetweenReads').show();
		$('#divBetweenReads').css('display','inline');
		$('#nreads').hide();
	}
	if ($('#nreads_sign').val()>0 && $('#nreads_sign').val()!=4){$('#nreads').show();$('#divBetweenReads').hide();}
}

function searchContigs(){
	flag=true;
	len=$('#length').val();
	if($('#length_sign').val()!=4 && !NumberInRange(len,0,6000)){ $('#val_length').show(250); flag=false;} 
	if ($('#length_sign').val()==4){
	len1=$('#length1').val(); len2=$('#length2').val();
		if(!NumberInRange(len1,0,6000) || !NumberInRange(len2,0,6000)){$('#val_length').show(250); flag=false;}
	}

	pgc=$('#gc').val();
	if($('#gc_sign').val()!=4 && !NumberInRange(pgc,0,100)){ $('#val_gc').show(250); flag=false;} 
	if ($('#gc_sign').val()==4){
	gc1=$('#gc1').val(); gc2=$('#gc2').val();
	if(!NumberInRange(gc1,0,100) || !NumberInRange(gc2,0,100)){ $('#val_gc').show(250); flag=false;	}
	}

	nr=$('#nreads').val();
	if($('#nreads_sign').val()!=4 && !NumberInRange(nr,0,1500)){ $('#val_nreads').show(250); flag=false;} 
	if ($('#nreads_sign').val()==4){
	nr1=$('#nreads1').val(); nr2=$('#nreads2').val();
	if(!NumberInRange(nr1,0,1500) || !NumberInRange(nr2,0,1500)){$('#val_nreads').show(250); flag=false;}
	}

	if(flag){$('#formContig').submit();} else {return false;}
}

function loadSearchTranslation(){
	if ($('#length_sign').val()==4){
		$('#divBetween').show();
		$('#divBetween').css('display','inline');
		$('#length').hide();
	}
	if ($('#length_sign').val()>0 && $('#length_sign').val()!=4){
		$('#length').show();
		$('#divBetween').hide();
	}
	if ($('#BH').attr('checked')==true){
		$('#evalue').css('display','inline');
		$('#evalue').show();
	}
}

function searchTranslations(){
	flag=true;
	len=$('#length').val();
	if($('#length_sign').val()!=4 && !NumberInRange(len,0,2000)){ $('#val_length').show(250); flag=false;} 
	evalue=$('#evalueField').val();

	if ($('#length_sign').val()==4){
	len1=$('#length1').val(); len2=$('#length2').val();
		if(!NumberInRange(len1,0,2000) || !NumberInRange(len2,0,2000)){ 
		$('#val_length').show(250); flag=false;}
	}
	if ($('#BH').attr('checked')==true){
		if(!NumberInRange(evalue,0,200)){$('#val_evalue').show(250);flag=false;}
	}
	if(flag){$('#formTranslation').submit();} else {return false;}
}
