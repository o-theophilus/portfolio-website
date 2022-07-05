<script>
	export let num;
	let n = Math.round(num / 10);
	let m = 10 - n;
</script>

{#each Array(n) as _, n}
	<div class="filled" />{/each}{#each Array(m) as _, n}
	<div class="empty" />
{/each}

<!-- {num} -->
<style>
	div {
		--size: 15px;

		display: inline-block;
		width: var(--size);
		height: var(--size);
		
		border-radius: 50%;

		margin: 0 1px;
	}
	.filled{
		background-color: var(--fColor3);
		
	}
	.empty{
border: 2px solid;
	}
</style>
