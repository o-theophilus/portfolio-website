<script>
	export let item;
	export let blog = false;

	let href;
	let target;

	if (item.type === 'link') {
		href = item.content;
		target = '_blank';
	} else if (item.type === 'doc') {
		href = `/docs/${item.content}`;
		target = '_blank';
	} else {
		href = `/${blog ? 'blog' : 'project'}/${item.slug}`;
	}
</script>

<a {href} {target}>
	<img src="/images/{item.image}" alt={item.image} />
	<div class="blocker" />
	<div class="block">
		<h3 class="title">
			{item.title}
		</h3>
		<div class="details">
			{#if item.summary}
				<p class="summary">
					{item.summary}
				</p>
			{/if}
			<p class="date">
				{item.date}
			</p>
		</div>
	</div>
</a>

<style>
	a {
		display: block;

		position: relative;

		height: 300px;

		text-decoration: none;
		color: var(--fColor2);

		border-radius: var(--bRadius);
		overflow: hidden;

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	a:not(:last-child) {
		margin-bottom: 50px;
	}
	a:hover .block {
		top: 0;
		background-color: rgba(0, 0, 0, 0.8);
	}
	a:hover .details {
		height: initial;
	}
	a:hover .title {
		color: var(--color3);
	}

	img {
		display: block;
		width: 100%;
		height: 100%;

		object-fit: cover;
	}

	.block {
		position: absolute;

		display: flex;
		flex-direction: column;
		justify-content: center;

		color: var(--color1);

		inset: 0;
		top: 80%;

		background-color: rgba(0, 0, 0, 0.3);
		text-align: center;

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;

		padding: 0 20px;
	}
	.details {
		height: 0;
		overflow: hidden;
	}
	.title {
		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	.date {
		font-size: 0.7em;
	}

	@media screen and (min-width: 500px) {
		.block {
			padding: 0 20%;
		}
	}
	@media screen and (min-width: 600px) {
		a {
			height: 400px;
			line-height: unset;
		}
	}
</style>
