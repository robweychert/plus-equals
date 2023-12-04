document.addEventListener('DOMContentLoaded', (event) => {

	function setAttrs(obj, attrSet) {
		const attrs = Object.keys(attrSet);
		for (i = 0; i < attrs.length; i++) {
			obj.setAttribute(attrs[i], attrSet[attrs[i]]);
		}
	}

	const canvasW = 600;
	const subgrid = 8;
	const margin = 6;
	const weight = 3/1000 * canvasW;
	const density = 12;
	let radialSymmetry = false;
	const svgId = 'foo';

	const grid = 4;
	const subgridUnit = canvasW / ((margin * 2) + (subgrid * grid));
	const gridUnit = subgridUnit * subgrid;
	const marginUnit = subgridUnit * margin;
	let deviationPairs = [
		[-2,-2],[-2,-1],[-2,0],[-2,1],[-2,2],
		[-1,-2],[-1,-1],[-1,0],[-1,1],[-1,2],
		[ 0,-2],[ 0,-1],[ 0,0],[ 0,1],[ 0,2],
		[ 1,-2],[ 1,-1],[ 1,0],[ 1,1],[ 1,2],
		[ 2,-2],[ 2,-1],[ 2,0],[ 2,1],[ 2,2]
	]
	let mutations = 0;
	let waveAmt = 0;

	const refresh = document.createElement('button');
	refresh.setAttribute('id', 'refresh');
	refresh.innerHTML = 'Regenerate';
	refresh.addEventListener('click', function (e) {
		e.preventDefault();
		refreshMutation();
	});
	document.getElementById('body').appendChild(refresh);

	const radialForm = document.createElement('form');
	const radialToggle = document.createElement('input');
	radialToggle.setAttribute('id', 'radial-toggle');
	radialToggle.setAttribute('type', 'checkbox');
	// radialToggle.setAttribute('checked', '');
	radialToggle.addEventListener('change', function(e) {
		radialSymmetry = !radialSymmetry;
		refreshMutation();
	});
	const radialLabel = document.createElement('label');
	radialLabel.setAttribute('for', 'radial-toggle');
	radialLabel.innerHTML = 'Radial symmetry';
	radialForm.appendChild(radialToggle);
	radialForm.appendChild(radialLabel);
	document.getElementById('body').appendChild(radialForm);

	function refreshMutation() {
		shuffle(deviationPairs);
		radial();
		console.log(deviationPairs);
		mutation(makeRows(deviationPairs));
	}

	function newSVG() {
		const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
		const svgAttrs = {
			'id': svgId,
			'width': canvasW,
			'height': canvasW,
			'viewBox': '0 0 ' + canvasW.toString() + ' ' + canvasW.toString()
		};
		setAttrs(svg, svgAttrs);

		const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
		const style = document.createElementNS('http://www.w3.org/2000/svg', 'style');
		style.innerHTML = 'rect{fill:white}path{fill:none;stroke:black;stroke-width:' + weight.toString() + ';stroke-linecap:round;}';
		defs.appendChild(style);
		svg.appendChild(defs);

		const bg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
		const bgAttrs = {
			'x': 0,
			'y': 0,
			'width': canvasW,
			'height': canvasW
		};
		setAttrs(bg, bgAttrs);
		svg.appendChild(bg);

		return svg;
	}

	// Shuffle an array
	// https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array/2450976#2450976
	function shuffle(array) {
		let currentIndex = array.length,  randomIndex;

		// While there remain elements to shuffle.
		while (currentIndex > 0) {

			// Pick a remaining element.
			let randomIndex = Math.floor(Math.random() * currentIndex);
			currentIndex--;

			// And swap it with the current element.
			[array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
		}
		return array;
	}

	// Adjust a list of deviation pairs to have radial symmetry
	function radial() {
		if (radialSymmetry) {
			const symmetryPairs = [];
			const negSymmetryPairs = [];
			for (let i = 0; i < deviationPairs.length; i++) {
				const negDeviationPair = [deviationPairs[i][0] * -1, deviationPairs[i][1] * -1];
				if (!(deviationPairs[i][0] == 0 && deviationPairs[i][1] == 0)) {
					let match = false;
					for (let j = 0; j < symmetryPairs.length; j++) {
						if ((deviationPairs[i][0] == symmetryPairs[j][0] && deviationPairs[i][1] == symmetryPairs[j][1]) || (deviationPairs[i][0] == negSymmetryPairs[j][0] && deviationPairs[i][1] == negSymmetryPairs[j][1])) {
							match = true;
						}
					}
					if (!(match)) {
						symmetryPairs.push(deviationPairs[i]);
						negSymmetryPairs.push(negDeviationPair);
					}
				}
				if (symmetryPairs.length >= 12) {
					break;
				}
			}
			negSymmetryPairs.reverse();
			symmetryPairs.push([0,0]);
			for (let i = 0; i < negSymmetryPairs.length; i++) {
				symmetryPairs.push(negSymmetryPairs[i]);
			}
			deviationPairs = symmetryPairs;
		}
	}

	// Divide a list of deviation pairs into rows
	function makeRows(pairList) {
		const rowList = []
		let row = []
		for (i=0; i < pairList.length; i++) {
			row.push(pairList[i]);
			if (row.length === grid + 1) {
				rowList.push(row);
				row = [];
			}
		}
		return rowList;
	}

	function mutation(rowList) {
		const svg = newSVG();
		const theseDeviationPairs = [];
		for (i=0; i < rowList.length; i++) {
			for (j=0; j < rowList[i].length; j++) {
				theseDeviationPairs.push(rowList[i][j]);
			}
		}
		mutations++;
		waveAmt = 0;
		let oldDStrings = [];
		const oldMutationNodes = document.querySelectorAll('#' + svgId + ' path');
		if (oldMutationNodes.length > 0) {
			for (i=0; i < oldMutationNodes.length; i++) {
				oldDStrings.push(oldMutationNodes[i].getAttribute('d'));
			}
		}
		const mutationRows = [];
		for (i=0; i < grid; i++) {
			for (j=0; j < density + 1; j++) {
				if (i === grid -1 || (i < grid - 1 && j < density)) {
					const thisRow = rowList[i];
					const nextRow = rowList[i+1];
					mutationRows.push([]);
					for (k=0; k < grid + 1; k++) {
	                    const x1 = marginUnit + (subgridUnit * thisRow[k][0]) + (gridUnit * k);
	                    const y1 = marginUnit + (subgridUnit * thisRow[k][1]) + (gridUnit * i);
	                    const x2 = marginUnit + (subgridUnit * nextRow[k][0]) + (gridUnit * k);
	                    const y2 = marginUnit + (subgridUnit * nextRow[k][1]) + (gridUnit * (i+1));
	                    const x  = x1 + (((x2 - x1) / density) * j);
	                    const y  = y1 + (((y2 - y1) / density) * j);
	                    mutationRows[mutationRows.length - 1].push([x,y])
					}
				}
			}
		}
		let rowLoop = 1;
		for (i=0; i < mutationRows.length; i++) {
			const row = mutationRows[i];
			const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
			path.setAttribute('id', 'wave' + waveAmt.toString());
			let dString = 'M ';
			for (j=0; j < row.length; j++) {
				if (j === 0) {
					dString += row[j][0].toString() + ' ' + row[j][1].toString();
				} else {
	                const xDif = row[j][0] - row[j-1][0];
	                const xDifUnit = xDif / 4;
	                let ctrlX = (xDifUnit * ((density - rowLoop) / density)) + xDifUnit;
	                if (rowLoop >= density / 2) {
	                	ctrlX = (xDifUnit * (rowLoop/density)) + xDifUnit;
	                }
	                dString += ' C ' 
	                	+ (row[j-1][0] + ctrlX).toString() 
	                	+ ' ' 
	                	+ row[j-1][1].toString()
	                	+ ', '
	                	+ (row[j][0] - ctrlX).toString()
	                	+ ' '
	                	+ row[j][1].toString()
	                	+ ', '
	                	+ row[j][0].toString()
	                	+ ' '
	                	+ row[j][1].toString();
				}
			}
			path.setAttribute('d', dString);
			if (mutations >= 2) {
				const animation = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
				animation.setAttribute('dur', '0.2s');
				animation.setAttribute('attributeName', 'd');
				animation.setAttribute('values', oldDStrings[waveAmt] + '; ' + dString);
				path.appendChild(animation);
			}
			svg.appendChild(path);
			if (rowLoop < density) {
				rowLoop++;
			} else {
				rowLoop = 1;
			}
			oldDStrings.push(dString);
			waveAmt++;
		}
		if (document.getElementById(svgId)) {
			document.getElementById(svgId).remove();
		}
		document.getElementById('body').appendChild(svg);
	}

	refreshMutation();

	// Render SVG on canvas for PNG/JPG download
	// https://developer.mozilla.org/en-US/docs/Web/API/Path2D/Path2D



	let no = 0;
	let yes = 0;
	const noLabel = '⬅️ No';
	const yesLabel = '➡️ Yes';
	const tindrDiv = document.createElement('div');
	const sectionNo = document.createElement('section');
	const sectionYes = document.createElement('section');
	const fieldNo = document.createElement('textarea');
	const fieldYes = document.createElement('textarea');
	const textNo = document.createElement('p');
	const textYes = document.createElement('p');
	textNo.innerHTML = noLabel + ': 0';
	textYes.innerHTML = yesLabel + ': 0';
	sectionNo.appendChild(textNo);
	sectionNo.appendChild(fieldNo);
	sectionYes.appendChild(textYes);
	sectionYes.appendChild(fieldYes);
	tindrDiv.appendChild(sectionNo);
	tindrDiv.appendChild(sectionYes);
	document.getElementById('body').appendChild(tindrDiv);

	function arrayToString(array) {
		let string = '[';
		for (let i = 0; i < array.length; i++) {
			string += ('[' + array[i][0] + ',' + array[i][1] + '],');
		}
		string += '],\n';
		return string;
	}
	function yesNo(choice) {
		if (choice == 'no') {
			no++;
			fieldNo.innerHTML = fieldNo.innerHTML + arrayToString(deviationPairs);
		} else {
			yes++;
			textYes.innerHTML = yesLabel + ': ' + yes.toString();
			fieldYes.innerHTML = fieldYes.innerHTML + arrayToString(deviationPairs);
			if (yes == 60) {
				window.alert('The Yes pile is full!');
			}
		}
		textNo.innerHTML = noLabel + ': ' + no.toString() + ' (' + Math.round((no / (no + yes)) * 100).toString() + '%)';
		textYes.innerHTML = yesLabel + ': ' + yes.toString() + ' (' + Math.round((yes / (no + yes)) * 100).toString() + '%)';
	}
	document.addEventListener('keyup', function (event) {
		if (event.defaultPrevented) {
			return;
		}
		let key = event.key || event.keyCode;
		if (key === 'ArrowLeft' || key === 37) {
			yesNo('no');
			refreshMutation();
		}
		if (key === 'ArrowRight' || key === 39) {
			yesNo('yes');
			refreshMutation();
		}
	});

});