<script>
	import { onDestroy, onMount } from 'svelte';

	let { data = [] } = $props();

	let canvas;
	let chart;

	onMount(() => {
		const labels = data.map((x) => x.label);
		const values = data.map((x) => x.value);

		chart = new Chart(canvas, {
			type: 'line',
			data: {
				labels,
				datasets: [
					{
						label: 'Sales',
						data: values,
						borderColor: '#3b82f6',
						backgroundColor: 'rgba(59,130,246,0.15)',
						fill: true,
						tension: 0.35,
						pointRadius: 4
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				scales: {
					y: {
						beginAtZero: true,
						ticks: { precision: 0 }
					}
				},
				plugins: {
					legend: { display: false }
				}
			}
		});
	});

	onDestroy(() => {
		if (chart) chart.destroy();
	});
</script>

<canvas bind:this={canvas}></canvas>

<style>
	canvas {
		width: 100% !important;
		height: 320px !important;
	}
</style>
