<script>
	import { page } from '$app/state';

	let { children } = $props();
</script>

<section
	style="
width: 100%;
max-width: 500px;
margin: auto;
"
>
	<div
		style="
		padding: 20px 40px;
		display: flex;
		"
	>
		<img
			src="{page.url.origin}/favicon.png"
			alt="favicon"
			style="
		width: 30px;
		height: 30px;
		"
		/>
		<b
			style="
		font-size: x-large;
		margin-left: 10px;
	"
			>Theophilus Ogbolu
		</b>
	</div>

	<div
		class="content"
		style="
	border: 2px solid #efefef;
	border-radius: 4px;
	padding: 40px;"
	>
		{@render children()}
	</div>
	<div
		class="footer"
		style="
	text-align: center;
	padding: 20px 40px;
	font-size: x-small;
	color: grey;"
	>
		&copy 2025 | Theophilus Ogbolu All rights reserved.
		<br />
		Design for impact
	</div>
</section>
