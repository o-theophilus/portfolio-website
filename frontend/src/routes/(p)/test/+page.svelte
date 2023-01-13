<script>
	import Content from '$lib/comp/content.svelte';

	let sticky;
	let block;
	let section;
	let scroller = {};
	let pos = {};

	const ooo = (scroller) =>
		(sticky.offsetTop / (section.clientHeight - sticky.clientHeight)) *
		(scroller.clientWidth - block.clientWidth);
</script>

<svelte:window
	on:scroll={(e) => {
		pos.a = ooo(scroller.a);
		pos.b = ooo(scroller.b);
	}}
/>
<Content>
	<section class="gap" />
</Content>
<section bind:this={section}>
	<div class="sticky" bind:this={sticky}>
		<Content>
			<div class="block" bind:this={block}>
				Project
				<div class="scroller" style:right="{pos.a}px" bind:this={scroller.a}>
					<div class="item">A</div>
					<div class="item">B</div>
					<div class="item">C</div>
					<div class="item">D</div>
					<div class="item">E</div>
					<div class="item">F</div>
				</div>
				Blog

				<div class="scroller left" style:left="{pos.b}px" bind:this={scroller.b}>
					<div class="item">A</div>
					<div class="item">B</div>
					<div class="item">C</div>
					<div class="item">F</div>
				</div>
			</div>
		</Content>
	</div>
</section>

<style>
	.gap {
		height: 100vh;
		color: green;
	}

	section {
		position: relative;
		height: 300vh;
	}
	.sticky {
		/* pointer-events: none; */
		position: sticky;

		top: 0;
	}
	.block {
		display: flex;
		flex-direction: column;
		justify-content: center;
		height: 100vh;
	}

	.scroller {
		position: relative;

		display: flex;
		gap: 10px;
		width: fit-content;
	}
	.left {
		align-self: flex-end;
	}

	.item {
		width: 400px;
		height: 30vh;
		flex-shrink: 0;

		background-color: blue;
	}
</style>
