<script>
	export let style = 1;
	export let color1 = '';
	export let color2 = '';
</script>

<svg
	viewBox="0 0 100 10"
	preserveAspectRatio="none"
	style:fill={`var(--${color1})`}
	style:background-color={`var(--${color2})`}
>
	{#if style == 1}
		<polygon points="0,0 100,10 0,10" />
	{:else if style == 2}
		<polygon points="100,0 100,10 0,10" />
	{:else if style == 3}
		<polygon points="0,0 100,0 0,10" />
	{:else if style == 4}
		<polygon points="0,0 100,0 100,10" />
	{/if}
</svg>

<style>
	svg {
		display: block;
		width: 100%;
		height: 90px;
	}
</style>
